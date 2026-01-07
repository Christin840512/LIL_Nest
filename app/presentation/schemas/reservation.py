from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional



# ---------- Reservation Schemas ----------

class ReservationDraft(BaseModel):
    """
    Draft a new reservation or update an existing one (partial update). :contentReference[oaicite:6]{index=6}
    """
    court_name: str = Field(min_length=1)
    start_time: datetime = Field(min_length=1)
    court_note: Optional[str] = None
    per_player_fee: Optional[int] = None
    paid_amount: Optional[int] = None
    bank_account: Optional[str] = None
    allow_multi_payer: Optional[bool] = None
    auto_issue_invoice: Optional[bool] = None
    players: Optional[List] = None

# class ReservationBase(BaseModel):
#     """
#     Base reservation schema (場次資訊).:contentReference[oaicite:2]{index=2}
#     Used when front-end sends '套用範本 -> 場次資訊 + 球友名單 + 繳費資訊'
#     """
#     court_name: str = Field(..., max_length=50)
#     court_note: Optional[str] = None  
#     players: List[ReservationPlayerCreate]
#     per_player_fee: int = 0
#     paid_amount: int = 0
#     allow_multi_payer: bool = False
#     auto_issue_invoice: bool = False


class ReservationConfirmed(ReservationDraft):
    """
    Used when when creating a new reservation (新增場次).:contentReference[oaicite:5]{index=5}
    """
    per_player_fee: int
    paid_amount: int
    bank_account: str
    allow_multi_payer: bool
    auto_issue_invoice: bool
    players: Optional[List[ReservationPlayerCreate]] = None




class ReservationRead(ReservationDraft):
    id: int
    user_id: int
    status: str
    created_at: datetime
    updated_at: datetime
    players: List[ReservationPlayerRead]
    payment_link: str

    class ConfigDict:
        from_attributes = True
