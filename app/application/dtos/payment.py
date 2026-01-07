from dataclasses import dataclass
from typing import Dict, Any, Optional
from domain.value_objects.payer_info import PayerInfo
from domain.value_objects.reservation_info import ReservationInfo


@dataclass(frozen=True)
class MpgFormField:
    merchant_id: str
    trade_info: Dict[str, Any]
    trade_sha: str
    version: str

@dataclass(frozen=True)
class MpgFormRequest:
    action_url: str
    fields: MpgFormField


@dataclass(frozen=True)
class MpgForm:
    merchant_order_no: str
    amount_twd: int
    item_desc: str
    notify_url: str
    return_url: Optional[str]
    customer_url: Optional[str]
    client_back_url: Optional[str]
    respond_type: Optional[str]               # "JSON" or "String"
    lang_type: Optional[str]        # "zh-tw"/"en"/"jp"
    enable_payments: Optional[Dict[str, int]]

    

@dataclass(frozen=True)
class NewebpayNotify:
    status: str
    merchant_id: str
    version: str
    trade_info_hex: str
    trade_sha: str
    result: Optional[Dict[str, Any]] # decrypted and parsed


@dataclass(frozen=True)
class CreatePaymentCommand:
    reservation_info: ReservationInfo
    payer_info: PayerInfo
    amount_twd: int
    item_desc: str

    notify_url: str
    return_url: Optional[str] = None
    customer_url: Optional[str] = None
    client_back_url: Optional[str] = None

    respond_type: str = "JSON"
    lang_type: Optional[str] = "zh-tw"
    enable_payments: Optional[Dict[str, int]] = None


@dataclass(frozen=True)
class CreatePaymentResult:
    merchant_order_no: str
    mpg_form_request: MpgFormRequest

@dataclass(frozen=True)
class HandleNotifyResult:
    ok: bool
    merchant_order_no: Optional[str] = None
    new_status: Optional[str] = None