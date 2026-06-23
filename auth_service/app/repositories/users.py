"""Репозиторий доступа к пользователям (только уровень БД).

Операции: get_by_id, get_by_email, create. Репозиторий не проверяет пароли,
не создаёт токены и не выбрасывает HTTPException. Возвращает данные/None либо
низкоуровневые ошибки БД.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User


class UsersRepository:
    """Доступ к таблице пользователей."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_email(self, email: str) -> User | None:
        """Найти пользователя по email или вернуть None."""
        result = await self._session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: int) -> User | None:
        """Найти пользователя по первичному ключу или вернуть None."""
        return await self._session.get(User, user_id)

    async def create(self, email: str, password_hash: str, role: str = "user") -> User:
        """Создать пользователя. Пароль приходит УЖЕ захешированным извне."""
        user = User(email=email, password_hash=password_hash, role=role)
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user
