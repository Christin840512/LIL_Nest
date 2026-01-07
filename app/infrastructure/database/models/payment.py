from __future__ import annotations

from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Enum, Index, JSON
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.models.base import Base
from domain.entities.payment import Payment, PaymentProvider, PaymentStatus


class PaymentModel(Base):
    __tablename__ = "payments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    
    reservation_id: Mapped[str] = mapped_column(String(64), index=True)
    player_id: Mapped[list[str]] = mapped_column(JSON, index=True)
    
    payer_name: Mapped[str] = mapped_column(String(100))
    payer_email: Mapped[str] = mapped_column(String(100))
    payer_phone: Mapped[str] = mapped_column(String(20))

    amount_twd: Mapped[int] = mapped_column(Integer)

    payment_provider: Mapped[PaymentProvider] = mapped_column(Enum(PaymentProvider), default=PaymentProvider.NEWEBPAY)
    status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus), default=PaymentStatus.CREATED)

    merchant_order_no: Mapped[str | None] = mapped_column(String(30), unique=True, index=True, nullable=True)
    trade_no: Mapped[str | None] = mapped_column(String(20), nullable=True)
    payment_type: Mapped[str | None] = mapped_column(String(20), nullable=True)
    pay_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())

    __table_args__ = (
        Index("ix_payments_reservation_status", "reservation_id", "status"),
    )

    