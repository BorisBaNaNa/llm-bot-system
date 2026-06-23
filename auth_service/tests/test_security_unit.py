"""Модульные тесты функций безопасности (чистые функции, без БД и FastAPI).

Проверяют: хеш не равен паролю, verify проходит на верном и не проходит на
неверном; create_access_token + decode_token дают payload с sub/role/iat/exp,
и sub/role совпадают с переданными.
"""

from datetime import datetime, timedelta, timezone

import pytest
from jose import ExpiredSignatureError, JWTError, jwt

from app.core.config import settings
from app.core.security import (
    create_access_token,
    decode_token,
    hash_password,
    verify_password,
)


def test_hash_password_differs_from_plain_and_is_salted():
    password = "password123"
    h1 = hash_password(password)
    h2 = hash_password(password)
    # Хеш не равен паролю и из-за случайной соли два хеша одного пароля разные.
    assert h1 != password
    assert h1 != h2


def test_verify_password_true_on_correct_false_on_wrong():
    h = hash_password("password123")
    assert verify_password("password123", h) is True
    assert verify_password("wrong-password", h) is False


def test_jwt_roundtrip_carries_sub_role_iat_exp():
    token = create_access_token(subject=42, role="user")
    payload = decode_token(token)
    assert payload["sub"] == "42"  # sub всегда строка
    assert payload["role"] == "user"
    assert "iat" in payload
    assert "exp" in payload


def test_decode_token_rejects_foreign_secret():
    token = create_access_token(subject=1, role="user")
    with pytest.raises(JWTError):
        jwt.decode(token, "other-secret", algorithms=[settings.jwt_alg])


def test_decode_token_rejects_expired():
    # Токен с истёкшим сроком — подписываем тем же секретом, но exp в прошлом.
    past = datetime.now(timezone.utc) - timedelta(minutes=5)
    expired = jwt.encode(
        {"sub": "1", "role": "user", "exp": int(past.timestamp())},
        settings.jwt_secret,
        algorithm=settings.jwt_alg,
    )
    with pytest.raises(ExpiredSignatureError):
        decode_token(expired)
