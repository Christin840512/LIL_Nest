from fastapi import HTTPException, status
from fastapi.responses import HTMLResponse, PlainTextResponse
from typing import Dict

from application.dtos.payment import CreatePaymentCommand, NewebpayNotify
from application.use_cases.payment import CreatePaymentUseCase, HandleNewebpayNotifyUseCase

import traceback



def create_payment_controller(cmd: CreatePaymentCommand, uc: CreatePaymentUseCase,
) -> str:
    result = uc.execute(cmd)
    # Return auto-submit HTML form
    inputs = "\n".join(
        f'<input type="hidden" name="{k}" value="{v}"/>'
        for k, v in result.mpg_form_request.fields.items()
    )
    html = f"""
    <html><body>
      <form id="newebpay" method="post" action="{result.mpg_form_request.action_url}">
        {inputs}
        <noscript><button type="submit">Continue to Pay</button></noscript>
      </form>
      <script>document.getElementById("newebpay").submit();</script>
    </body></html>
    """
    return HTMLResponse(content=html)


def handle_newebpay_notify_controller(cmd: NewebpayNotify, uc: HandleNewebpayNotifyUseCase) -> PlainTextResponse:
    try:
        uc.execute(cmd)
    except Exception as e:
        print(traceback.format_exc())
        

    return PlainTextResponse(content="OK", status_code=200)
        