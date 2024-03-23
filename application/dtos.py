from pydantic import BaseModel


class CreatePaymentRequest(BaseModel):
    amount: float


class CreatePaymentResponse(BaseModel):
    id: str
    amount: float
    status: str
    reference_id: str
    