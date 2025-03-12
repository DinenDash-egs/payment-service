from fastapi import FastAPI, APIRouter, Query
from models import PaymentRequest, PaymentResponse, PaymentStatusUpdate, Method, Status
from main import create_payment, update_payment_status, get_payment_status, delete_payment, get_filtered_payments

app = FastAPI(
    title="Payment API",
    version="1.0",
    description="API responsável pelo processamento de pagamentos."
)

router = APIRouter(prefix="/v1")

# Criar um novo pagamento
@router.post("/payments", response_model=PaymentResponse, summary="Criar um novo pagamento")
async def create_payment_endpoint(payment: PaymentRequest):
    return await create_payment(payment)

# Atualizar status do pagamento
@router.put("/payments", summary="Atualizar status do pagamento")
async def update_payment_status_endpoint(update: PaymentStatusUpdate):
    return await update_payment_status(update)

# Obter status de um pagamento específico
@router.get("/payments/{payment_id}", response_model=PaymentResponse, summary="Obter status de um pagamento")
async def get_payment_status_endpoint(payment_id: str):
    return await get_payment_status(payment_id)

# **Novo GET: Filtrar pagamentos com validação dos parâmetros**
@router.get("/payments", summary="Filtrar pagamentos")
async def get_filtered_payments_endpoint(
    status: Status = Query(None, description="Filtrar pagamentos pelo status"),
    method: Method = Query(None, description="Filtrar pagamentos pelo método"),
    limit: int = Query(10, description="Número máximo de resultados"),
    offset: int = Query(0, description="Número de resultados a ignorar antes de começar a listar")
):
    return await get_filtered_payments(status, method, limit, offset)

# Deletar um pagamento
@router.delete("/payments/{payment_id}", summary="Deletar um pagamento")
async def delete_payment_endpoint(payment_id: str):
    return await delete_payment(payment_id)

app.include_router(router)

# Health Check para saber se o serviço está ativo
@app.get("/", summary="Health Check")
async def root():
    return {"message": "Payment Service is running"}
