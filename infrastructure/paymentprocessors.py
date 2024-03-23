import json
from abc import ABC, abstractmethod
from domain import models
from infrastructure import dtos
import requests
import base64


PAYPAL_CLIENT_ID = ""
PAYPAL_SECRET = ""
PAYPAL_BASE = ""


class PaymentProcessor(ABC):
    @abstractmethod
    async def create_payment(self, payment, reference_id):
        pass


class PaypalPaymentProcessor(PaymentProcessor):
    async def create_payment(self, payment: models.Payment, reference_id: str):
        jwt = self.get_paypal_jwt()

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {jwt}",
        }

        paypal_purchase_unit = dtos.PaypalPurchaseUnit(reference_id, dtos.PaypalAmount("USD", str(payment.amount)))

        purchase_units = [paypal_purchase_unit]

        paypal_create_order_request = dtos.PaypalCreateOrderRequest("CAPTURE", purchase_units)

        response: requests.Response = requests.post(PAYPAL_BASE + "v2/checkout/orders", data=json.dumps(paypal_create_order_request.as_dict()), headers=headers)

        payment_processor_response = dtos.PaymentProcessorCreateOrderResponse()
        payment_processor_response.id = response.json()["id"]
        payment_processor_response.status = response.json()["status"]

        return payment_processor_response

    def get_paypal_jwt(self):
        encoded_credentials = base64.b64encode(bytes(f"{PAYPAL_CLIENT_ID}:{PAYPAL_SECRET}", "utf-8")).decode("ascii")

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {encoded_credentials}"
        }

        paypal_authentication_request = {
            "grant_type": "client_credentials"
        }

        response = requests.post(PAYPAL_BASE + "v1/oauth2/token", data=paypal_authentication_request, headers=headers)

        return response.json()["access_token"]
