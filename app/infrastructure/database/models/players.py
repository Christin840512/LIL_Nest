from __future__ import annotations
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, Integer

from base import Base
from reservations import ReservationParticipant
from typing import List
from payment import Payment


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    display_name: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

# relationships
    participations: Mapped[List["ReservationParticipant"]] = relationship(
        back_populates="player",
        cascade="all, delete-orphan",
    )
    payments_made: Mapped[List["Payment"]] = relationship(
        back_populates="payer",
        cascade="all, delete-orphan",
        foreign_keys="Payment.payer_player_id",
    )


