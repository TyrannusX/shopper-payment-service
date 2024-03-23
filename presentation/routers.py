from fastapi import APIRouter
from application import dtos, handlers
from infrastructure import repositories, paymentprocessors

# Dependencies
payment_router = APIRouter()
payment_processor = paymentprocessors.PaypalPaymentProcessor()
payment_repository = repositories.PaymentRepository()
create_payment_handler = handlers.CreatePaymentHandler(payment_processor, payment_repository)


@payment_router.post("/payments/")
async def create_payment(create_payment_request: dtos.CreatePaymentRequest):
    return await create_payment_handler.handle(create_payment_request)
