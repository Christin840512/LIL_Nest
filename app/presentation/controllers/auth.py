from fastapi import HTTPException, status

from application.dtos.auth import LoginCommand, GetAdminQuery
from application.use_cases.auth import LoginUseCase, GetAdminUseCase
from domain.exceptions.auth import InvalidCredentials, AdminRequired
from presentation.schemas.auth import LoginRequest, TokenResponse, UserRead


    
def login_controller(cmd: LoginCommand, uc: LoginUseCase) -> TokenResponse:
    try:
        result = uc.execute(cmd)
        return TokenResponse(access_token=result.access_token, token_type=result.token_type)

    except InvalidCredentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_admin_controller(cmd: GetAdminQuery, uc: GetAdminUseCase) -> UserRead:
    try:
        result = uc.execute(cmd)
        return UserRead(id=result.id, username=result.username)

    except AdminRequired:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges are required",
        )
   



