"""Эндпоинты Auth Service (/auth/*).

Тонкие маршруты: принимают вход, вызывают usecase, возвращают результат.
Без SQL и без прямой генерации токенов. Маршруты: /auth/register, /auth/login
(через OAuth2PasswordRequestForm = Depends()), /auth/me.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import AuthUseCaseDep, CurrentUserId
from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED
)
async def register(payload: RegisterRequest, auth: AuthUseCaseDep) -> UserPublic:
    """Зарегистрировать пользователя (занятый email -> 409)."""
    return await auth.register(payload.email, payload.password)


@router.post("/login", response_model=TokenResponse)
async def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth: AuthUseCaseDep,
) -> TokenResponse:
    """Войти по email (username) и паролю, получить JWT (неверные данные -> 401)."""
    token = await auth.login(form.username, form.password)
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserPublic)
async def me(user_id: CurrentUserId, auth: AuthUseCaseDep) -> UserPublic:
    """Вернуть профиль текущего пользователя по токену."""
    return await auth.me(user_id)
