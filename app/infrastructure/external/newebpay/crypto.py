from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Dict
from urllib.parse import urlencode, parse_qsl

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend



def aes256_cbc_encrypt_hex(plain: bytes, key: bytes, iv: bytes) -> str:
    padder = padding.PKCS7(128).padder()
    padded = padder.update(plain) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    enc = cipher.encryptor()
    ct = enc.update(padded) + enc.finalize()
    return ct.hex()


def aes256_cbc_decrypt_hex(cipher_hex: str, key: bytes, iv: bytes) -> bytes:
    ct = bytes.fromhex(cipher_hex)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    dec = cipher.decryptor()
    padded = dec.update(ct) + dec.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    plain = unpadder.update(padded) + unpadder.finalize()
    return plain


def newebpay_trade_sha(hash_key: str, hash_iv: str, trade_info_hex: str) -> str:
    # SHA256("HashKey={key}&{TradeInfoHex}&HashIV={iv}") upper-case
    raw = f"HashKey={hash_key}&{trade_info_hex}&HashIV={hash_iv}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest().upper()


def build_urlencoded_query(data: Dict[str, str | int]) -> str:
    # Newebpay uses http_build_query-like encoding (URL-encoded)
    # Keep doseq False; values are scalar.
    return urlencode({k: str(v) for k, v in data.items()}, safe="*-_.", encoding="utf-8")


def parse_urlencoded_query(qs: str) -> Dict[str, str]:
    # parse_qsl preserves ordering; return last value for duplicated keys.
    return {k: v for k, v in parse_qsl(qs, keep_blank_values=True, encoding="utf-8")}
