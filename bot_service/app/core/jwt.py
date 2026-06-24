"""Проверка JWT в Bot Service (только валидация, без выпуска).

decode_and_validate(token: str) -> dict: проверяет подпись и exp, возвращает
payload (с sub). При неверном или истёкшем токене бросает ValueError или
доменное исключение. Токены здесь НЕ создаются.
"""

from jose import ExpiredSignatureError, JWTError, jwt

from app.core.config import settings


def decode_and_validate(token: str) -> dict:
    """Проверить чужой JWT и вернуть его payload.

    Подпись сверяется общим с auth_service секретом, срок действия (exp)
    проверяет сам python-jose. Дополнительно требуем непустой sub - без него
    непонятно, чей это токен. Любая проблема - это ValueError с понятным
    текстом, который хэндлер покажет пользователю. Новые токены тут не выдаются.
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_alg],
        )
    except ExpiredSignatureError as exc:
        raise ValueError("Токен истёк, авторизуйтесь заново") from exc
    except JWTError as exc:
        raise ValueError("Невалидный токен") from exc

    if not payload.get("sub"):
        raise ValueError("В токене нет sub")

    return payload
