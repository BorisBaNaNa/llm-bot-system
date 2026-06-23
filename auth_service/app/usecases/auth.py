"""Бизнес-логика Auth Service.

register(), login(), me(): проверка существования пользователя, хеширование и
проверка пароля, создание JWT, получение профиля. При ошибках бросаются
исключения из core/exceptions.py (UserAlreadyExistsError, InvalidCredentialsError,
UserNotFoundError). Без прямого SQL - только вызовы репозитория.
"""

from app.core.exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.core.security import create_access_token, hash_password, verify_password
from app.db.models import User
from app.repositories.users import UsersRepository


class AuthUseCase:
    """Сценарии регистрации, логина и получения профиля."""

    def __init__(self, users: UsersRepository) -> None:
        self._users = users

    async def register(self, email: str, password: str) -> User:
        """Зарегистрировать нового пользователя."""
        if await self._users.get_by_email(email) is not None:
            raise UserAlreadyExistsError()
        password_hash = hash_password(password)
        return await self._users.create(email=email, password_hash=password_hash)

    async def login(self, email: str, password: str) -> str:
        """Проверить учётные данные и вернуть подписанный JWT access token."""
        user = await self._users.get_by_email(email)
        # Одинаковая ошибка на оба случая, чтобы не раскрывать, есть ли email.
        if user is None or not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()
        return create_access_token(subject=user.id, role=user.role)

    async def me(self, user_id: int) -> User:
        """Вернуть профиль пользователя по id."""
        user = await self._users.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError()
        return user
