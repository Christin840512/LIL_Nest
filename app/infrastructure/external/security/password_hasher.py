from passlib.context import CryptContext
from domain.ports.password_hasher import PasswordHasher

_pwd_ctx = CryptContext(schemes=["bcrypt_sha256", "bcrypt"], deprecated="auto")


class BcryptPasswordHasher(PasswordHasher):
    def verify(self, plain_password: str, password_hash: str) -> bool:
        return _pwd_ctx.verify(plain_password, password_hash)
