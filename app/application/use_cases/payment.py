from __future__ import annotations
import time

from dataclasses import dataclass
from typing import Dict, Optional
from uuid import uuid4

from infrastructure.database.repositories.payment import PaymentRepository
from domain.entities.payment import Payment
from application.dtos.payment import CreatePaymentCommand, CreatePaymentResult, MpgForm, NewebpayNotify, HandleNotifyResult
from domain.ports.payment_repository import IPaymentRepository
from domain.ports.payment_gateway import PaymentGateway, NewebpayNotify
from datetime import datetime
from domain.enums.payment import PaymentStatus, PaymentProvider


############# Use Case: Create Payment #############

class CreatePaymentUseCase:
    def __init__(self, repo: IPaymentRepository, gateway: PaymentGateway):
        self.repo = repo
        self.gateway = gateway

    def execute(self, cmd: CreatePaymentCommand) -> CreatePaymentResult:
        if cmd.amount_twd <= 0:
            raise ValueError("amount_twd must be positive")


        # MerchantOrderNo needs to be unique, <= 30 chars typically.
        # Use a deterministic + unique scheme:
        raw = f"RES{cmd.reservation_info.id}-{int(time.time())}".replace("-", "")
        merchant_order_no = raw[:30]

        payment = Payment(
            id=merchant_order_no,
            reservation_info=cmd.reservation_info,
            payer_info=cmd.payer_info,
            amount_twd=cmd.amount_twd,
            status=PaymentStatus.PENDING,
            payment_provider=PaymentProvider.NEWEBPAY,
            merchant_order_no=merchant_order_no,
            trade_no="",
            payment_type="",
            pay_time=datetime.now,
        )
        payment.mark_pending()
        self.repo.add(payment)


        mpg_form = MpgForm(
            merchant_order_no=merchant_order_no,
            amount_twd=cmd.amount_twd,
            item_desc=cmd.item_desc,
            notify_url=cmd.notify_url,
            return_url=cmd.return_url,
            customer_url=cmd.customer_url,
            client_back_url=cmd.client_back_url,
            respond_type=cmd.respond_type,
            lang_type=cmd.lang_type,
            enable_payments=cmd.enable_payments,
        )              

        mpg_form_request = self.gateway.build_mpg_form(mpg_form=mpg_form)

        return CreatePaymentResult(
            merchant_order_no=merchant_order_no,
            mpg_form_request=mpg_form_request,
        )


############# Use Case: Handle Payment Notification #############


class HandleNewebpayNotifyUseCase:
    def __init__(self, repo: IPaymentRepository, gateway: PaymentGateway):
        self.repo = repo
        self.gateway = gateway

    def execute(self, cmd: NewebpayNotify) -> HandleNotifyResult:
        notify = self.gateway.parse_and_verify_notify(cmd)

        # decrypted result often includes these
        merchant_order_no = str(notify.result.get("MerchantOrderNo") or "")
        trade_no = str(notify.result.get("TradeNo") or "")
        payment_type = str(notify.result.get("PaymentType") or "")
        pay_time_raw = notify.result.get("PayTime")

        payment = self.repo.get_by_id(merchant_order_no)
        if not payment:
            # Don't explode; caller (route) should still return 200
            return HandleNotifyResult(ok=False, merchant_order_no=merchant_order_no)

        # Idempotency: if already paid, ignore repeats
        if payment.status == PaymentStatus.PAID and notify.status == "SUCCESS":
            return HandleNotifyResult(ok=True, merchant_order_no=merchant_order_no, new_status=payment.status.value)

        if notify.status == "SUCCESS":
            pay_time = None
            if isinstance(pay_time_raw, str) and pay_time_raw.strip():
                safe = pay_time_raw.replace("+", " ")
                try:
                    pay_time = datetime.strptime(safe, "%Y-%m-%d %H:%M:%S")
                except Exception:
                    pay_time = None
            payment.mark_paid(trade_no=trade_no, payment_type=payment_type, pay_time=pay_time)
        else:
            payment.mark_failed()

        self.repo.update(payment)
        return HandleNotifyResult(
            ok=True,
            merchant_order_no=merchant_order_no,
            new_status=payment.status.value,
        )

