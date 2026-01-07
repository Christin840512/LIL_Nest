from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from domain.entities.payment import Payment
from domain.enums.payment import PaymentStatus
from domain.ports.payment_repository import IPaymentRepository
from infrastructure.database.models.payment import PaymentModel


def _to_entity(m: PaymentModel) -> Payment:
    return Payment(
        id=m.id,
        reservation_info=m.reservation_id,
        payer_id=m.payer_id,
        amount_twd=m.amount_twd,
        status=PaymentStatus(m.status),
        payment_provider=m.provider,
        merchant_order_no=m.merchant_order_no,
        trade_no=m.trade_no,
        payment_type=m.payment_type,
        pay_time=m.pay_time,
        created_at=m.created_at,
        updated_at=m.updated_at,
    )


def _apply_model(m: PaymentModel, e: Payment) -> None:
    m.reservation_id = e.reservation_info.id
    m.player_id = e.reservation_info.players
    m.payer_name = e.payer_info.name
    m.payer_email = e.payer_info.email
    m.payer_phone = e.payer_info.phone
    m.amount_twd = e.amount_twd
    m.payment_provider = e.payment_provider
    m.status = e.status.value
    m.merchant_order_no = e.merchant_order_no
    m.trade_no = e.trade_no
    m.payment_type = e.payment_type
    m.pay_time = e.pay_time
    m.created_at = e.created_at
    m.updated_at = e.updated_at


class PaymentRepository(IPaymentRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def add(self, payment: Payment) -> None:
        m = PaymentModel(id=payment.id)
        _apply_model(m, payment)
        self.db.add(m)
        # self.db.commit()

    def get_by_id(self, payment_id: str) -> Optional[Payment]:
        m = self.db.get(PaymentModel, payment_id)
        return _to_entity(m) if m else None

    # def get_by_merchant_order_no(self, merchant_order_no: str) -> Optional[Payment]:
    #     m = (
    #         self.db.query(PaymentModel)
    #         .filter(PaymentModel.merchant_order_no == merchant_order_no)
    #         .first()
    #     )
    #     return _to_entity(m) if m else None

    def update(self, payment: Payment) -> None:
        m = self.db.get(PaymentModel, payment.id)
        if not m:
            # if you prefer raising domain exception, do it in use case
            return
        _apply_model(m, payment)
        self.db.commit()
