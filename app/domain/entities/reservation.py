from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

from app.domain.entities.player import Player
from app.domain.enums.reservation import ReservationStatus, PaymentMethod, PaymentStatus

@dataclass
class Reservation:
    id: int
    starts_at: datetime
    court_name: str
    court_note: Optional[str]
    fee_per_person: int
    paid_amount: int
    bank_account: str
    allow_multi_payer: bool
    auto_issue_invoice: bool
    players: List[Player]
    status: str
    created_at: datetime
    updated_at: datetime

    def record_update(self) -> None:
        self.updated_at = datetime.now()
    
    def record_creation(self) -> None:
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def confirm(self) -> None:
        # Logic to confirm the reservation
        pass
    
    def cancel(self) -> None:
        # Logic to cancel the reservation
        pass
    
    def edit(self) -> None:
        # Logic to edit the reservation
        if self.status != ReservationStatus.EDITING:
            self.status = ReservationStatus.EDITING

    def change_status(self, new_status: str) -> None:
        self.status = new_status
        
    
