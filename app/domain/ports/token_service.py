from abc import ABC, abstractmethod
from typing import Dict, Any

class TokenService(ABC):
    @abstractmethod
    def create_access_token(self, claims: Dict[str, Any]) -> str:
        raise NotImplementedError

    def decode_access_token(self, token: str) -> Dict[str, Any]:
        raise NotImplementedError