from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, JSONResponse

from presentation.schemas.payment import PayerInfo as PayerInfoSchema
from domain.value_objects.payer_info import PayerInfo as PayerInfoEntity
from domain.value_objects.reservation_info import ReservationInfo as ReservationInfoEntity
from presentation.schemas.payment import ReservationInfo as ReservationInfoSchema
from application.use_cases.payment import CreatePaymentCommand, CreatePaymentUseCase
from application.use_cases.payment import HandleNewebpayNotifyUseCase
from presentation.schemas.payment import CreatePaymentIn, NewebpayNotify
from presentation.controllers.payment import (
    create_payment_controller,
    handle_newebpay_notify_controller,
)

from presentation.dependencies.payment import (
    get_create_payment_uc,
    get_notify_uc,
)

router = APIRouter(tags=["payments"])



@router.post("/payment/checkout", response_class=HTMLResponse)
def create_mpg_payment(
    payload: CreatePaymentIn,
    uc: CreatePaymentUseCase = Depends(get_create_payment_uc)) -> HTMLResponse:
    cmd = CreatePaymentCommand(
            reservation_info=ReservationInfoEntity(id=payload.reservation_info.id, players=payload.reservation_info.players),
            payer_info=PayerInfoEntity(name=payload.payer_info.name, email=payload.payer_info.email, phone=payload.payer_info.phone),
            amount_twd=payload.amount_twd,
            item_desc=payload.item_desc,
            notify_url=payload.notify_url,
            return_url=payload.return_url,
            customer_url=payload.customer_url,
            client_back_url=payload.client_back_url,
            enable_payments=payload.enable_payments,
        )
    return create_payment_controller(cmd, uc)
    



@router.post("/newebpay/notify", response_class=PlainTextResponse)
async def newebpay_notify(
    request: Request,
    uc: HandleNewebpayNotifyUseCase = Depends(get_notify_uc)) -> PlainTextResponse:
    # Newebpay posts form-data
    notify = await request.form()
    print("Received newebpay notify:", notify)
    cmd = NewebpayNotify(
        status=notify.get("Status", ""),
        merchant_id=notify.get("MerchantID", ""),
        version=notify.get("Version", ""),
        trade_info_hex=notify.get("TradeInfo", ""),
        trade_sha=notify.get("TradeSha", ""),
    )
    return handle_newebpay_notify_controller(cmd, uc)    



# @router.post("/newebpay/return", response_class=JSONResponse)
# async def newebpay_return(
#     request: Request,
#     gw: NewebpayClient = Depends(get_payment_gateway),  # gateway singleton
# ) -> JSONResponse:
#     form = await request.form()
#     data = {k: str(v) for k, v in form.items()}
#     parsed = gw.parse_and_verify_notify(data)
#     return JSONResponse({"status": parsed.status, "result": parsed.result})


# @router.get("/newebpay/query/{merchant_order_no}", response_class=JSONResponse)
# async def query_trade_info(
#     merchant_order_no: str,
#     amt: int,
#     gw: NewebpayClient = Depends(get_payment_gateway),
# ) -> JSONResponse:
#     result = await gw.query_trade_info(merchant_order_no, noted_amt := int(amt))
#     return JSONResponse({"merchant_order_no": merchant_order_no, "amt": noted_amt, "result": result})
