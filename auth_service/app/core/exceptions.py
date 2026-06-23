"""HTTP-исключения Auth Service.

BaseHTTPException наследуется от fastapi.HTTPException, от него - конкретные
доменные исключения с нужными кодами. Минимум: UserAlreadyExistsError (409),
InvalidCredentialsError (401), InvalidTokenError (401), TokenExpiredError (401),
UserNotFoundError (404), PermissionDeniedError (403). Используются в usecases и
deps вместо ручных raise HTTPException.
"""

from fastapi import HTTPException, status


class BaseHTTPException(HTTPException):
    """Базовое исключение: код и текст задаются на уровне класса-наследника.

    Так usecases/deps бросают говорящее доменное исключение
    (raise UserAlreadyExistsError()), а FastAPI сам отдаёт нужный HTTP-ответ.
    """

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "Внутренняя ошибка сервера"

    def __init__(self, detail: str | None = None) -> None:
        super().__init__(status_code=self.status_code, detail=detail or self.detail)


class UserAlreadyExistsError(BaseHTTPException):
    """Регистрация на уже занятый email."""

    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь с таким email уже существует"


class InvalidCredentialsError(BaseHTTPException):
    """Неверная пара email/пароль при логине."""

    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный email или пароль"


class InvalidTokenError(BaseHTTPException):
    """Токен повреждён, подделан или имеет неверный формат."""

    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Недействительный токен"


class TokenExpiredError(BaseHTTPException):
    """Срок действия токена истёк."""

    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Срок действия токена истёк"


class UserNotFoundError(BaseHTTPException):
    """Пользователь не найден."""

    status_code = status.HTTP_404_NOT_FOUND
    detail = "Пользователь не найден"


class PermissionDeniedError(BaseHTTPException):
    """Недостаточно прав для операции."""

    status_code = status.HTTP_403_FORBIDDEN
    detail = "Недостаточно прав"
