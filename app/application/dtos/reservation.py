from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass(frozen=True)
class ReservationCreateCommand:
    starts_at: datetime
    court_name: str
    court_note: Optional[str]
    players: List[str]
    fee_per_person: int
    bank_account: Optional[str]
    allow_multi_payer: bool
    auto_issue_invoice: bool
    paid_amount: int


@dataclass(frozen=True)
class ReservationResult:
    id: int
    starts_at: datetime
    court_name: str
    court_note: Optional[str]
    players: List[str]
    fee_per_person: int
    bank_account: str
    allow_multi_payer: bool
    auto_issue_invoice: bool
    paid_amount: int
    status: str
    created_at: datetime
    updated_at: datetime

