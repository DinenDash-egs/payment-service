from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException
import os
from models import PaymentRequest, PaymentStatusUpdate

# Configuração do MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/paymentdb")
client = AsyncIOMotorClient(MONGO_URI)
db = client.paymentdb
payments_collection = db["payments"]

# Criar pagamento
async def create_payment(payment: PaymentRequest):
    payment_data = {
        "order_id": payment.order_id,
        "amount": payment.amount,
        "method": payment.method.value,  # Extraindo o valor do Enum
        "status": "pending"
    }
    result = await payments_collection.insert_one(payment_data)
    return {"payment_id": str(result.inserted_id), "status": "pending"}

# Atualizar status do pagamento
async def update_payment_status(update: PaymentStatusUpdate):
    result = await payments_collection.update_one(
        {"_id": update.payment_id}, {"$set": {"status": update.status.value}}  # Usar o Enum corretamente
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Payment not found")
    return {"message": f"Payment {update.payment_id} updated to {update.status.value}"}

# Obter status de um pagamento específico
async def get_payment_status(payment_id: str):
    payment = await payments_collection.find_one({"_id": payment_id})
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return {
        "payment_id": payment_id,
        "status": payment["status"],
        "amount": payment["amount"],
        "method": payment["method"],
    }

# Filtrar pagamentos com base no status e método
async def get_filtered_payments(status=None, method=None, limit=10, offset=0):
    query = {}
    if status:
        query["status"] = status
    if method:
        query["method"] = method

    payments = await payments_collection.find(query).skip(offset).limit(limit).to_list(length=limit)
    return payments

# Deletar pagamento
async def delete_payment(payment_id):
    result = await payments_collection.delete_one({"_id": payment_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Payment not found")
    return {"message": f"Payment {payment_id} deleted"}
