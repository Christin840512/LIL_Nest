from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, Optional, Any
from application.dtos.payment import MpgForm, MpgFormRequest, NewebpayNotify



class PaymentGateway(ABC):
    @abstractmethod
    def build_mpg_form(self, form: Dict[str, str]) -> MpgFormRequest: ...

    @abstractmethod
    def parse_and_verify_notify(self, form: Dict[str, str]) -> NewebpayNotify: ...

    @abstractmethod
    def build_query_payload(self, merchant_order_no: str, amount_twd: int) -> Dict[str, str]: ...

    @abstractmethod
    def create_check_value(self, merchant_order_no: str, amount_twd: int) -> str: ...