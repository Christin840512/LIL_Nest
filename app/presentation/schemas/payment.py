from pydantic import BaseModel, Field
from typing import Dict, Optional, Any
from domain.value_objects.payer_info import PayerInfo
from domain.value_objects.reservation_info import ReservationInfo



class ReservationInfo(BaseModel):
    id: str
    players: list[str]

class PayerInfo(BaseModel):
    name: str
    email: str
    phone: str



class CreatePaymentIn(BaseModel):
    reservation_info: ReservationInfo
    payer_info: PayerInfo
    amount_twd: int = Field(ge=1)
    item_desc: str = Field(min_length=1, max_length=50)
    notify_url: str
    return_url: Optional[str] = None
    customer_url: Optional[str] = None
    client_back_url: Optional[str] = None
    enable_payments: Optional[Dict[str, int]] = None

class NewebpayNotify(BaseModel):
    status: str
    merchant_id: str
    version: str
    trade_info_hex: str
    trade_sha: str
    # result: Dict[str, Any]  # decrypted and parsed


class HandleNotifyResult(BaseModel):
    ok: bool
    merchant_order_no: Optional[str] = None
    new_status: Optional[str] = None