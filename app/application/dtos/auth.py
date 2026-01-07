from dataclasses import dataclass


@dataclass(frozen=True)
class LoginCommand:
    username: str
    password: str


@dataclass(frozen=True)
class TokenResult:
    access_token: str
    token_type: str = "bearer"

@dataclass(frozen=True)
class GetAdminQuery:
    id: int

@dataclass(frozen=True)
class AdminResult:
    id: int
    username: str
