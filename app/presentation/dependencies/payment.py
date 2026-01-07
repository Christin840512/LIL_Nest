from __future__ import annotations

from functools import lru_cache
from fastapi import Depends
from sqlalchemy.orm import Session

from infrastructure.config.settings import Settings, get_settings
from infrastructure.database.session import get_db
from infrastructure.database.repositories.payment import PaymentRepository

from infrastructure.external.newebpay.client import NewebpayClient

from domain.ports.payment_repository import IPaymentRepository
from domain.ports.payment_gateway import PaymentGateway

from application.use_cases.payment import CreatePaymentUseCase
from application.use_cases.payment import HandleNewebpayNotifyUseCase
from application.dtos.payment import MpgForm





def get_payment_gateway(settings: Settings = Depends(get_settings)) -> NewebpayClient:
    # gateway is stateless -> singleton is fine
    return NewebpayClient(
        settings=settings,
    )


# ---- request-scoped ----
def get_payment_repo(db: Session = Depends(get_db)) -> PaymentRepository:
    return PaymentRepository(db)


# ---- use cases ----
def get_create_payment_uc(
    repo: PaymentRepository = Depends(get_payment_repo),
    gw: PaymentGateway = Depends(get_payment_gateway),
) -> CreatePaymentUseCase:
    return CreatePaymentUseCase(repo=repo, gateway=gw)


def get_notify_uc(
    repo: PaymentRepository = Depends(get_payment_repo),
    gw: PaymentGateway = Depends(get_payment_gateway),
) -> HandleNewebpayNotifyUseCase:
    return HandleNewebpayNotifyUseCase(repo=repo, gateway=gw)
