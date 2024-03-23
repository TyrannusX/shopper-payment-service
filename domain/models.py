from enum import Enum


class PaymentStatuses(Enum):
    NEW = 1
    FULFILLED = 2


class Payment:
    id: str
    amount: float
    status: str
    payment_processor_id: str
    payment_processor_status: str

    def __init__(self):
        pass
