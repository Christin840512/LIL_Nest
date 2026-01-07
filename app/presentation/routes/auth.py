from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from application.dtos.auth import GetAdminQuery, LoginCommand
from application.use_cases.auth import LoginUseCase, GetAdminUseCase
from presentation.controllers.auth import login_controller, get_admin_controller
from presentation.schemas.auth import LoginRequest, TokenResponse, UserRead
from presentation.dependencies.auth import get_login_use_case, get_current_admin_id, get_admin_use_case


router = APIRouter(tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    uc: LoginUseCase = Depends(get_login_use_case),
) -> TokenResponse:
    cmd = LoginCommand(username=form.username, password=form.password)
    return login_controller(cmd, uc)

@router.get("/me", response_model=UserRead)
def read_current_user(
    payload: int = Depends(get_current_admin_id),
    uc: GetAdminUseCase = Depends(get_admin_use_case),
) -> UserRead:
    cmd = GetAdminQuery(id=payload)
    return get_admin_controller(cmd, uc)

