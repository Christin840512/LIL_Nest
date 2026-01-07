from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from domain.exceptions.auth import InvalidCredentials
from domain.ports.password_hasher import PasswordHasher
from domain.ports.token_service import TokenService
from domain.ports.user_repository import IAdminUserRepository
from application.dtos.auth import LoginCommand, TokenResult, GetAdminQuery, AdminResult


@dataclass
class LoginUseCase:
    repo: IAdminUserRepository
    hasher: PasswordHasher
    token_service: TokenService
    access_token_ttl_minutes: int = 30

    def execute(self, cmd: LoginCommand) -> TokenResult:
        user = self.repo.get_admin(cmd.username)

        if user is None:
            raise InvalidCredentials()

        if not self.hasher.verify(cmd.password, user.password_hash):
            raise InvalidCredentials()

        now = datetime.now(timezone.utc)
        user.record_login(now)
        self.repo.save_admin(user)

        token = self.token_service.create_access_token(
            subject=user.username,
            id=user.id,
            expires_delta=timedelta(minutes=self.access_token_ttl_minutes),
        )
        return TokenResult(access_token=token)
    
@dataclass
class GetAdminUseCase:
    repo: IAdminUserRepository
    def execute(self, query: GetAdminQuery) -> AdminResult:
        user = self.repo.get_by_id(query.id)
        if not user:
            return None
        return AdminResult(
            id=user.id,
            username=user.username,
        )
