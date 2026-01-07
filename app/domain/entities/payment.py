from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from domain.enums.payment import PaymentProvider, PaymentStatus, PaymentMethod
from domain.value_objects.payer_info import PayerInfo
from domain.value_objects.reservation_info import ReservationInfo

@dataclass
class Payment:
    id: str  # same as merchant_order_no
    reservation_info: ReservationInfo
    payer_info: PayerInfo
    amount_twd: int
    status: PaymentStatus
    # Newebpay specific info
    payment_provider: PaymentProvider
    merchant_order_no: Optional[str]
    trade_no: str
    payment_type: PaymentMethod
    pay_time: datetime

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def mark_pending(self) -> None:
        self.status = PaymentStatus.PENDING
        self.updated_at = datetime.now

    def mark_paid(
        self,
        trade_no: str,
        payment_type: str,
        pay_time: Optional[datetime] = None,
    ) -> None:
        self.status = PaymentStatus.PAID
        self.trade_no = trade_no
        self.payment_type = payment_type
        self.pay_time = pay_time
        self.updated_at = datetime.now

    def mark_failed(self) -> None:
        self.status = PaymentStatus.FAILED
        self.updated_at = datetime.now

    def mark_refund_pending(self) -> None:
        self.status = PaymentStatus.REFUND_PENDING
        self.updated_at = datetime.now

    def mark_refunded(self) -> None:
        self.status = PaymentStatus.REFUNDED
        self.updated_at = datetime.now
