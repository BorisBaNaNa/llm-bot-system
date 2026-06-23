"""Зависимости FastAPI для Auth Service.

get_db() выдаёт AsyncSession; фабрики get_users_repo() и get_auth_uc();
get_current_user_id()/get_current_user() берёт токен из Authorization: Bearer,
декодирует и проверяет его, возвращает user_id/пользователя. При ошибках токена
бросает InvalidTokenError / TokenExpiredError.
"""

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import InvalidTokenError, TokenExpiredError
from app.core.security import decode_token
from app.db.session import AsyncSessionLocal
from app.repositories.users import UsersRepository
from app.usecases.auth import AuthUseCase


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Выдать сессию БД на время запроса и гарантированно закрыть её после."""
    async with AsyncSessionLocal() as session:
        yield session


# Короткий алиас, чтобы не повторять Depends(get_db) в каждом провайдере.
SessionDep = Annotated[AsyncSession, Depends(get_db)]


def get_users_repo(session: SessionDep) -> UsersRepository:
    return UsersRepository(session)


def get_auth_uc(
    users: Annotated[UsersRepository, Depends(get_users_repo)],
) -> AuthUseCase:
    return AuthUseCase(users)


# tokenUrl — путь эндпоинта логина (для кнопки Authorize в Swagger).
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user_id(token: Annotated[str, Depends(oauth2_scheme)]) -> int:
    """Достать user_id из JWT.

    Просроченный токен -> TokenExpiredError, битый или без sub -> InvalidTokenError
    (оба наследуют HTTPException и дают 401).
    """
    try:
        payload = decode_token(token)
    except ExpiredSignatureError as exc:
        raise TokenExpiredError() from exc
    except JWTError as exc:
        raise InvalidTokenError() from exc
    sub = payload.get("sub")
    if sub is None:
        raise InvalidTokenError()
    return int(sub)


# Готовые зависимости для роутеров.
AuthUseCaseDep = Annotated[AuthUseCase, Depends(get_auth_uc)]
CurrentUserId = Annotated[int, Depends(get_current_user_id)]
