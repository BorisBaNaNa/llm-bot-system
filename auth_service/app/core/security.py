"""Функции безопасности Auth Service.

bcrypt через passlib: hash_password() и verify_password().
JWT через python-jose: create_access_token() (payload с sub, role, iat, exp) и
decode_token() (валидация подписи и срока). Используются как строительные блоки
в usecases и deps. Без БД и без знания про роуты.
"""

from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

# Контекст хеширования: алгоритм bcrypt. deprecated="auto" позволит в будущем
# завести новые схемы и автоматически помечать старые хеши как устаревшие.
_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Вернуть bcrypt-хеш пароля (со случайной солью внутри)."""
    return _pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Проверить, что пароль соответствует ранее сохранённому хешу."""
    return _pwd_context.verify(password, password_hash)


def create_access_token(subject: str, role: str) -> str:
    """Создать подписанный JWT access token.

    В payload кладём: sub (id пользователя), role, iat (выдан) и exp (истекает).
    Срок жизни берётся из настроек, подпись - секретом JWT_SECRET.
    """
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {
        "sub": str(subject),
        "role": role,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_alg)


def decode_token(token: str) -> dict:
    """Расшифровать и проверить токен (подпись + срок действия).

    Возвращает payload. Если токен невалиден или просрочен, python-jose
    выбрасывает jose.JWTError - перевод этой ошибки в HTTP 401 делает слой API.
    """
    return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_alg])
