from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status

from domain.exceptions.auth import InvalidToken
from application.use_cases.auth import LoginUseCase, GetAdminUseCase
from infrastructure.database.session import get_db
from infrastructure.config.settings import Settings, get_settings
from infrastructure.database.repositories.user import AdminUserRepository
from infrastructure.external.security.password_hasher import BcryptPasswordHasher
from infrastructure.external.security.jwt_token import JwtTokenService


def get_login_use_case(
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> LoginUseCase:
    repo = AdminUserRepository(db)
    hasher = BcryptPasswordHasher()
    token_service = JwtTokenService(secret_key=settings.jwt.JWT_SECRET_KEY, algorithm=settings.jwt.JWT_ALGORITHM)
    return LoginUseCase(
        repo=repo,
        hasher=hasher,
        token_service=token_service,
        access_token_ttl_minutes=30,
    )



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_admin_id(
    token: str = Depends(oauth2_scheme),
    settings: Settings = Depends(get_settings),
) -> int:
    token_service = JwtTokenService(secret_key=settings.jwt.JWT_SECRET_KEY, algorithm=settings.jwt.JWT_ALGORITHM)
    try:
        payload = token_service.decode_access_token(token)
        admin_id: int = payload.get("id")
        if admin_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return admin_id
    except InvalidToken:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_admin_use_case(
    db: Session = Depends(get_db),
) -> GetAdminUseCase:
    repo = AdminUserRepository(db)
    return GetAdminUseCase(repo=repo)
