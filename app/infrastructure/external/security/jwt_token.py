from __future__ import annotations
from datetime import datetime, timedelta, timezone
import jwt

from domain.ports.token_service import TokenService


class JwtTokenService(TokenService):
    def __init__(self, secret_key: str, algorithm: str):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_access_token(self, subject: str, id: int, expires_delta: timedelta) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": subject,
            "id": id,
            "iat": int(now.timestamp()),
            "exp": int((now + expires_delta).timestamp()),
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def decode_access_token(self, token: str) -> dict:
        return jwt.decode(token, self.secret_key, algorithms=self.algorithm)







