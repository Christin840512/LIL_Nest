from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional
from domain.entities.payment import Payment


class IPaymentRepository(ABC):
    @abstractmethod
    def add(self, payment: Payment) -> None: ...

    @abstractmethod
    def get_by_id(self, payment_id: str) -> Optional[Payment]: ...

    # @abstractmethod
    # def get_by_merchant_order_no(self, merchant_order_no: str) -> Optional[Payment]: ...

    @abstractmethod
    def update(self, payment: Payment) -> None: ...
