from __future__ import annotations

import json
import time
import httpx
import hashlib

from dataclasses import dataclass
from typing import Any, Dict, Optional
from urllib.parse import unquote_plus

from infrastructure.config.settings import get_settings
from application.dtos.payment import MpgForm, MpgFormRequest
from domain.ports.payment_gateway import PaymentGateway
from application.dtos.payment import MpgFormRequest, NewebpayNotify
from infrastructure.external.newebpay.crypto import (
    aes256_cbc_encrypt_hex,
    aes256_cbc_decrypt_hex,
    newebpay_trade_sha,
    build_urlencoded_query,
    parse_urlencoded_query,
)



class NewebpayClient(PaymentGateway):
    """
    Implements Newebpay MPG (front-stage) + notify decrypt/verify + QueryTradeInfo + creditcard cancel/close + ewallet refund.
    Based on NDNF-1.1.9 doc: AES-256-CBC PKCS7 + hex, SHA256 upper-case checks. :contentReference[oaicite:1]{index=1}
    """

    def __init__(self, settings):
        self.secrets = settings.newebpay_secrets
        self.endpoints = settings.newebpay_endpoints

    @property
    def mpg_url(self) -> str:
        return self.endpoints.MPG

    @property
    def query_url(self) -> str:
        return self.endpoints.QUERY
    
    @property
    def cancel_url(self) -> str:
        return self.endpoints.CANCEL

    @property
    def close_url(self) -> str:
        return self.endpoints.CLOSE
    
    @property
    def ewallet_refund_url(self) -> str:
        return self.endpoints.EWALLET_REFUND

    def build_mpg_form(
        self,
        mpg_form: MpgForm
    ) -> MpgFormRequest:
        # TradeInfo inner params per 4.2.1 (MerchantID, RespondType, TimeStamp, Version, MerchantOrderNo, Amt, ItemDesc, ...)
        trade_info: Dict[str, Any] = {
            "MerchantID": self.secrets.MERCHANT_ID,
            "RespondType": mpg_form.respond_type,          # "JSON" or "String"
            "TimeStamp": int(time.time()),
            "Version": "2.3",                  # doc says 2.3
            "MerchantOrderNo": mpg_form.merchant_order_no,
            "Amt": int(mpg_form.amount_twd),
            "ItemDesc": mpg_form.item_desc,
            "NotifyURL": mpg_form.notify_url,             # do NOT set same as ReturnURL (doc warning)
        }
        if mpg_form.lang_type:
            trade_info["LangType"] = mpg_form.lang_type
        if mpg_form.return_url:
            trade_info["ReturnURL"] = mpg_form.return_url
        if mpg_form.customer_url:
            trade_info["CustomerURL"] = mpg_form.customer_url
        if mpg_form.client_back_url:
            trade_info["ClientBackURL"] = mpg_form.client_back_url

        if mpg_form.enable_payments:
            # Example: {"CREDIT":1,"VACC":1,"WEBATM":1,"CVS":1}
            for k, v in mpg_form.enable_payments.items():
                trade_info[k] = int(v)

        qs = build_urlencoded_query(trade_info).encode("utf-8")

        trade_info_hex = aes256_cbc_encrypt_hex(
            plain=qs,
            key=self.secrets.HASH_KEY.encode("utf-8"),
            iv=self.secrets.HASH_IV.encode("utf-8"),
        )
        trade_sha = newebpay_trade_sha(self.secrets.HASH_KEY, self.secrets.HASH_IV, trade_info_hex)

        # outer form fields per 4.2.1: MerchantID, TradeInfo, TradeSha, Version
        fields = {
            "MerchantID": self.secrets.MERCHANT_ID,
            "TradeInfo": trade_info_hex,
            "TradeSha": trade_sha,
            "Version": "2.3",
            # EncryptType omitted => AES/CBC/PKCS7 (doc)
        }
        return MpgFormRequest(action_url=self.mpg_url, fields=fields)

    def parse_and_verify_notify(self, form: NewebpayNotify) -> NewebpayNotify:
        # Newebpay notify/return returns: Status, MerchantID, Version, TradeInfo, TradeSha (4.2.2)
        status = form.status
        merchant_id = form.merchant_id
        version = form.version
        trade_info_hex = form.trade_info_hex
        trade_sha = form.trade_sha

        expected = newebpay_trade_sha(self.secrets.HASH_KEY, self.secrets.HASH_IV, trade_info_hex)
        if expected != trade_sha:
            raise ValueError("Invalid TradeSha (SHA256 check failed)")

        plain = aes256_cbc_decrypt_hex(
            cipher_hex=trade_info_hex,
            key=self.secrets.HASH_KEY.encode("utf-8"),
            iv=self.secrets.HASH_IV.encode("utf-8"),
        ).decode("utf-8", errors="replace")

        # plain is urlencoded query string, values may contain + for space
        # Example: "...&PayTime=2023-09-27+14%3A21%3A59&..."
        decoded = unquote_plus(plain)
        data = parse_urlencoded_query(decoded)

        # RespondType=JSON case: Status/Message/Result may appear flattened or Result content in JSON.
        # Many merchants just treat it as a flat query string; keep as dict.
        return NewebpayNotify(
            status=status,
            merchant_id=merchant_id,
            version=version,
            trade_info_hex=trade_info_hex,
            trade_sha=trade_sha,
            result=data,
        )

    # ---------- QueryTradeInfo (NPA-B02) ----------

    def build_query_payload(
        self,
        merchant_order_no: str,
        amount_twd: int,
        respond_type: str = "JSON",
        version: str = "1.3",
    ) -> Dict[str, str]:
        """
        Post fields per 4.3.1: MerchantID, Version, RespondType, CheckValue, TimeStamp, MerchantOrderNo, Amt
        CheckValue rule per 4.1.6: SHA256("IV={iv}&{sorted(Amt,MerchantID,MerchantOrderNo)}&Key={key}") upper-case
        """
        ts = int(time.time())
        check_value = self._check_value(merchant_order_no=merchant_order_no, amt=amount_twd)
        return {
            "MerchantID": self.secrets.MERCHANT_ID,
            "Version": version,
            "RespondType": respond_type,
            "CheckValue": check_value,
            "TimeStamp": str(ts),
            "MerchantOrderNo": merchant_order_no,
            "Amt": str(int(amount_twd)),
        }

    def create_check_value(self, merchant_order_no: str, amount_twd: int) -> str:
        # sort keys by A~Z: Amt, MerchantID, MerchantOrderNo
        parts = {
            "Amt": str(int(amount_twd)),
            "MerchantID": self.secrets.MERCHANT_ID,
            "MerchantOrderNo": merchant_order_no,
        }
        # deterministic: build query with sorted keys
        data1 = "&".join([f"{k}={parts[k]}" for k in sorted(parts.keys())])
        raw = f"IV={self.secrets.HASH_IV}&{data1}&Key={self.secrets.HASH_KEY}".encode("utf-8")
        return hashlib.sha256(raw).hexdigest().upper()

    async def query_trade_info(self, merchant_order_no: str, amount_twd: int) -> Dict[str, Any]:
        payload = self.build_query_payload(merchant_order_no, amount_twd)
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.post(self.query_url, data=payload)
            r.raise_for_status()
            # Newebpay returns JSON if RespondType=JSON, else string
            try:
                return r.json()
            except Exception:
                return {"raw": r.text}

    # ---------- CreditCard Cancel (NPA-B01) ----------

    def build_creditcard_cancel_auth_payload(
        self,
        merchant_order_no: str,
        amount_twd: int,
        index_type: int = 1,
        trade_no: Optional[str] = None,
        respond_type: str = "JSON",
        version: str = "1.0",
    ) -> Dict[str, str]:
        """
        Post fields per 4.4.1: MerchantID_, PostData_ (AES256 http-encoded)
        PostData_ includes: RespondType, Version, TimeStamp, Amt, MerchantOrderNo or TradeNo, IndexType
        """
        inner: Dict[str, Any] = {
            "RespondType": respond_type,
            "Version": version,
            "TimeStamp": int(time.time()),
            "Amt": int(amount_twd),
            "IndexType": int(index_type),
        }
        if index_type == 1:
            inner["MerchantOrderNo"] = merchant_order_no
        elif index_type == 2:
            if not trade_no:
                raise ValueError("trade_no required when index_type=2")
            inner["TradeNo"] = trade_no
        else:
            raise ValueError("index_type must be 1 or 2")

        qs = build_urlencoded_query(inner).encode("utf-8")
        postdata_hex = aes256_cbc_encrypt_hex(qs, self.secrets.HASH_KEY.encode(), self.secrets.HASH_IV.encode())
        return {"MerchantID_": self.secrets.MERCHANT_ID, "PostData_": postdata_hex}

    # ---------- CreditCard Close (B031~B034) ----------

    def build_creditcard_close_payload(
        self,
        merchant_order_no: str,
        amount_twd: int,
        close_type: int,
        cancel: bool = False,
        index_type: int = 1,
        trade_no: Optional[str] = None,
        respond_type: str = "JSON",
        version: str = "1.1",
    ) -> Dict[str, str]:
        """
        Post fields per 4.5.1: MerchantID_, PostData_
        PostData_ includes: RespondType, Version, Amt, MerchantOrderNo, TimeStamp, IndexType, CloseType, (Cancel=1 optional), (TradeNo if IndexType=2)
        close_type: 1=請款/取消請款, 2=退款/取消退款
        """
        inner: Dict[str, Any] = {
            "RespondType": respond_type,
            "Version": version,
            "Amt": int(amount_twd),
            "MerchantOrderNo": merchant_order_no,
            "TimeStamp": int(time.time()),
            "IndexType": int(index_type),
            "CloseType": int(close_type),
        }
        if cancel:
            inner["Cancel"] = 1

        if index_type == 2:
            if not trade_no:
                raise ValueError("trade_no required when index_type=2")
            inner["TradeNo"] = trade_no

        qs = build_urlencoded_query(inner).encode("utf-8")
        postdata_hex = aes256_cbc_encrypt_hex(qs, self.secrets.HASH_KEY.encode(), self.secrets.HASH_IV.encode())
        return {"MerchantID_": self.secrets.MERCHANT_ID, "PostData_": postdata_hex}

    # ---------- EWallet Refund (NPA-B06) ----------

    def build_ewallet_refund_payload(
        self,
        merchant_order_no: str,
        amount_twd: int,
        payment_type: str,
        respond_type: str = "JSON",
        version: str = "1.1",
    ) -> Dict[str, str]:
        """
        Post fields per 4.6.1: UID_, Version_, EncryptData_, RespondType_, HashData_
        EncryptData_ is AES256(JSON-string) hex; HashData_ is SHA256("HashKey={key}&{EncryptData_}&HashIV={iv}") upper-case
        """
        inner = {
            "MerchantOrderNo": merchant_order_no,
            "Amount": str(int(amount_twd)),
            "TimeStamp": str(int(time.time())),
            "PaymentType": payment_type,
        }
        json_str = json.dumps(inner, ensure_ascii=False, separators=(",", ":"))
        encrypt_hex = _aes256_cbc_encrypt_hex(json_str.encode("utf-8"), self.secrets.hash_key.encode(), self.secrets.hash_iv.encode())
        hash_data = newebpay_trade_sha(self.secrets.hash_key, self.secrets.hash_iv, encrypt_hex)

        return {
            "UID_": self.secrets.merchant_id,
            "Version_": version,
            "EncryptData_": encrypt_hex,
            "RespondType_": respond_type,
            "HashData_": hash_data,
        }
