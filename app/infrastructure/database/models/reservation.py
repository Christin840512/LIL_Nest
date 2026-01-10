from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, Integer, ForeignKey, Boolean, func, Enum
from domain.enums.reservation import ReservationStatus

from .base import Base
from .player import Player
from .payment import PaymentModel

class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status: Mapped[ReservationStatus] = mapped_column(Enum(ReservationStatus), nullable=False, default=ReservationStatus.UNPAID)
    court_name: Mapped[str] = mapped_column(String, nullable=False)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    fee_per_person: Mapped[int] = mapped_column(Integer, nullable=False)
    total_amount_twd: Mapped[int] = mapped_column(Integer, nullable=False)
    allow_multi_payer: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")
    auto_issue_invoice: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )

    players: Mapped[List["ReservationParticipant"]] = relationship(back_populates={"reservation_id"}, cascade="all, delete-orphan")
    payments: Mapped[List["PaymentModel"]] = relationship(back_populates={"reservation_id"}, cascade="all, delete-orphan")


class ReservationParticipant(Base):
    __tablename__ = "reservation_participants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    reservation_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("reservations.id", ondelete="CASCADE"),
        nullable=False,
    )
    player_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("players.id", ondelete="RESTRICT"),
        nullable=False,
    )
    payment_id: Mapped[Optional[str]] = mapped_column(
        String,
        ForeignKey("payments.id", ondelete="SET NULL"),
        nullable=True,
    )






