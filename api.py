from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from main import create_payment, update_payment_status, get_payment_status, delete_payment, get_filtered_payments  # Importa funções do main.py

app = FastAPI()

router = APIRouter()

router = APIRouter(prefix="/v1")

class PaymentRequest(BaseModel):
    order_id: str
    amount: float
    method: str  # "credit_card", "paypal", "bank_transfer"

class PaymentStatusUpdate(BaseModel):
    payment_id: str
    status: str  # "approved", "rejected", "pending"

@router.post("/payments")
async def create_payment_endpoint(payment: PaymentRequest):
    return await create_payment(payment)

@router.put("/payments")
async def update_payment_status_endpoint(update: PaymentStatusUpdate):
    return await update_payment_status(update)

@router.get("/payments/{payment_id}")
async def get_payment_status_endpoint(payment_id: str):
    return await get_payment_status(payment_id)

@router.get("/payments")
async def get_filtered_payments_endpoint(status: str = None, method: str = None, limit: int = 10, offset: int = 0):
    return await get_filtered_payments(status, method, limit, offset)

@router.delete("/payments/{payment_id}")
async def delete_payment_endpoint(payment_id: str):
    return await delete_payment(payment_id)

app.include_router(router)
