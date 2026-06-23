"""Pydantic-схемы регистрации и токенов.

RegisterRequest (email + password), TokenResponse (access_token + token_type).
При желании LoginResponse. Для /auth/login используется OAuth2PasswordRequestForm,
поэтому отдельная схема входа для логина может не требоваться.
"""

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """Тело запроса на регистрацию."""

    email: EmailStr
    # Верхняя граница 72 — лимит bcrypt в байтах (длиннее обрезается).
    password: str = Field(min_length=8, max_length=72)


class TokenResponse(BaseModel):
    """Ответ с выданным JWT access token."""

    access_token: str
    token_type: str = "bearer"
