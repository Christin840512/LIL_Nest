from enum import Enum

class PaymentProvider(str, Enum):
    NEWEBPAY = "newebpay"


class PaymentStatus(str, Enum):
    CREATED = "created"        # 已建立（尚未送出到藍新）
    PENDING = "pending"        # 已導向 MPG / 等待付款結果
    PAID = "paid"              # 付款成功
    FAILED = "failed"          # 付款失敗
    CANCELED = "canceled"      # 取消授權/取消付款（視金流狀態）
    REFUND_PENDING = "refund_pending"
    REFUNDED = "refunded"

class PaymentMethod(str, Enum):
    CREDIT_CARD = "credit_card"
    ATM = "atm"
    LINEPAY = "linepay"


