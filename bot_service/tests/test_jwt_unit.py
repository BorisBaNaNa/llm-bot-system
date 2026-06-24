"""Модульные тесты валидации JWT в Bot Service.

Токен, созданный тем же секретом и алгоритмом, успешно проходит
decode_and_validate, и sub извлекается корректно. Мусорная строка вместо токена
вызывает ошибку (бот не верит любому тексту).
"""

import pytest
from jose import jwt

from app.core.config import settings
from app.core.jwt import decode_and_validate


def test_decode_valid_token():
    """Токен на общем секрете проходит проверку, sub читается корректно."""
    token = jwt.encode(
        {"sub": "7", "role": "user"},
        settings.jwt_secret,
        algorithm=settings.jwt_alg,
    )

    payload = decode_and_validate(token)

    assert payload["sub"] == "7"


def test_decode_garbage_raises():
    """Любой текст вместо токена бот не принимает - это ValueError."""
    with pytest.raises(ValueError):
        decode_and_validate("not-a-real-jwt")
