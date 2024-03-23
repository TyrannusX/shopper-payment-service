class PaypalAuthenticationRequest:
    def __init__(self, grant_type):
        self.grant_type = grant_type


class PaypalAmount:
    def __init__(self, currency_code: str, value: str):
        self.currency_code = currency_code
        self.value = value


class PaypalPurchaseUnit:
    def __init__(self, reference_id: str, amount: PaypalAmount):
        self.reference_id = reference_id
        self.amount = amount


class PaypalCreateOrderRequest:
    def __init__(self, intent: str, purchase_units: list[PaypalPurchaseUnit]):
        self.intent = intent
        self.purchase_units = purchase_units

    def as_dict(self):
        d = {}

        d["intent"] = self.intent
        d["purchase_units"] = []

        for entry in self.purchase_units:
            d["purchase_units"].append({
                "reference_id": entry.reference_id,
                "amount": {
                    "currency_code": entry.amount.currency_code,
                    "value": entry.amount.value
                }
            })

        return d


class PaymentProcessorCreateOrderResponse:
    id: str
    status: str
