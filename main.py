from motor.motor_asyncio import AsyncIOMotorClient
import uuid
import os
from fastapi import HTTPException

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/paymentdb")
client = AsyncIOMotorClient(MONGO_URI)
db = client.paymentdb
payments_collection = db["payments"]

async def create_payment(payment):
    try:
        payment_id = str(uuid.uuid4())
        payment_data = {
            "payment_id": payment_id,
            "order_id": payment.order_id,
            "amount": payment.amount,
            "method": payment.method,
            "status": "pending"
        }
        result = await payments_collection.insert_one(payment_data)  # Aguardar inserção
        if not result.inserted_id:
            raise HTTPException(status_code=500, detail="Failed to insert payment")

        return {"payment_id": payment_id, "status": "pending"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def update_payment_status(update):
    payment = await payments_collection.find_one({"payment_id": update.payment_id})
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    await payments_collection.update_one(
        {"payment_id": update.payment_id},
        {"$set": {"status": update.status}}
    )
    return {"message": f"Payment {update.payment_id} updated to {update.status}"}

async def get_payment_status(payment_id):
    payment = await payments_collection.find_one({"payment_id": payment_id})
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    return {"payment_id": payment_id, "status": payment["status"], "amount": payment["amount"], "method": payment["method"]}

async def get_filtered_payments(status=None, method=None, limit=10, offset=0):
    query = {}
    if status:
        query["status"] = status
    if method:
        query["method"] = method

    payments = await payments_collection.find(query).skip(offset).limit(limit).to_list(length=limit)
    return payments

async def delete_payment(payment_id):
    result = await payments_collection.delete_one({"payment_id": payment_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Payment not found")

    return {"message": f"Payment {payment_id} deleted"}
