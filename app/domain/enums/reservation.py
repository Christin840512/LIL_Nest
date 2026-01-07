from enum import Enum

class ReservationStatus(str, Enum):
    EDITING = "editing"
    INCOMPLETE = "incomplete"
    UNPAID = "unpaid"
    PAID_PARTIAL = "paid_partial"
    PAID_ALL = "paid_all"

class PaymentStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    CANCELED = "canceled"

class PaymentMethod(str, Enum):
    CREDIT_CARD = "credit card"
    ATM = "atm"
    LINEPAY = "linepay"
