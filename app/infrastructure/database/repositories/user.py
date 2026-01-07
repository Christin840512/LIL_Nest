from __future__ import annotations
from sqlalchemy.orm import Session

from domain.entities.user import AdminUser
from domain.ports.user_repository import IAdminUserRepository
from infrastructure.database.models.user import UserModel


def _to_domain(m: UserModel) -> AdminUser:
    return AdminUser(
        id=m.id,
        username=m.username,
        password_hash=m.password_hash,
        last_login_at=m.last_login_at,
    )


class AdminUserRepository(IAdminUserRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_admin(self, username: str) -> AdminUser | None:
        m = self.db.query(UserModel).filter(UserModel.username == username).first()
        return _to_domain(m) if m else None

    def save_admin(self, user: AdminUser) -> None:
        m = self.db.get(UserModel, user.id)
        if not m:
            return
        m.last_login_at = user.last_login_at
        self.db.add(m)
        self.db.commit()

    def get_by_id(self, id: int) -> AdminUser | None:
        m = self.db.get(UserModel, id)
        return _to_domain(m) if m else None

