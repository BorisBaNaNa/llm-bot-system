"""Публичное представление пользователя.

UserPublic: id, email, role, created_at (с from_attributes). В схеме ответа
никогда не должно быть password_hash.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserPublic(BaseModel):
    """Безопасное представление пользователя для ответов API (без хеша пароля)."""

    # from_attributes=True — собирать схему из атрибутов ORM-объекта User.
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    role: str
    created_at: datetime
