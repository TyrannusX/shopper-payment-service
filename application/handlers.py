from abc import ABC, abstractmethod

import application.dtos
import infrastructure.dtos
from infrastructure import paymentprocessors, repositories, dtos
from domain import models
from application import dtos, exceptions
from uuid import uuid4


class Handler(ABC):
    @abstractmethod
    async def handle(self, dto):
        pass


class CreatePaymentHandler(Handler):
    def __init__(self, payment_processor: paymentprocessors.PaymentProcessor, payment_repository: repositories.CrudRepository):
        self.payment_processor = payment_processor
        self.payment_repository = payment_repository

    async def handle(self, create_payment_request: dtos.CreatePaymentRequest):
        payment = models.Payment()
        payment.id = None
        payment.amount = create_payment_request.amount
        payment.status = str(models.PaymentStatuses.NEW)

        self.validate_payment_amount(payment)

        reference_id = str(uuid4())

        payment_processor_response: infrastructure.dtos.PaymentProcessorCreateOrderResponse = await self.payment_processor.create_payment(payment, reference_id)
        payment.payment_processor_id = payment_processor_response.id
        payment.payment_processor_status = payment_processor_response.status

        payment_id = await self.payment_repository.create(payment)
        payment.id = payment_id

        return application.dtos.CreatePaymentResponse(id=payment.id, amount=payment.amount, status=payment.status, reference_id=reference_id)

    def validate_payment_amount(self, payment: models.Payment):
        if payment.amount < 0.0:
            raise exceptions.BadRequestException("Payment amount cannot be negative!")
