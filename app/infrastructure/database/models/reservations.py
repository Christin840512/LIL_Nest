from typing import List, Optional
from __future__ import annotations
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, Integer, ForeignKey, Boolean

from .base import Base
from .players import Player
from .payments import Payment

class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    court_name: Mapped[str] = mapped_column(String, nullable=False)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    fee_per_person: Mapped[int] = mapped_column(Integer, nullable=False)
    allow_multi_payer: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")
    auto_issue_invoice: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=datetime.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=datetime.now(),
        onupdate=datetime.now(),
    )

    participants: Mapped[List["ReservationParticipant"]] = relationship(
        back_populates="reservation",
        cascade="all, delete-orphan",
    )

    payments: Mapped[List["Payment"]] = relationship(
        back_populates="reservation",
        cascade="all, delete-orphan",
    )


class ReservationParticipant(Base):
    __tablename__ = "reservation_participants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

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

    fee_due: Mapped[int] = mapped_column(Integer, nullable=False)
    role: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=DateTime.now(),
    )

    reservation: Mapped["Reservation"] = relationship(back_populates="participants")
    player: Mapped["Player"] = relationship(back_populates="participations")

    allocations: Mapped[List["PaymentAllocation"]] = relationship(
        back_populates="participant",
        cascade="all, delete-orphan",
    )





