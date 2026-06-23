"""HTTP-исключения Auth Service.

BaseHTTPException наследуется от fastapi.HTTPException, от него - конкретные
доменные исключения с нужными кодами. Минимум: UserAlreadyExistsError (409),
InvalidCredentialsError (401), InvalidTokenError (401), TokenExpiredError (401),
UserNotFoundError (404), PermissionDeniedError (403). Используются в usecases и
deps вместо ручных raise HTTPException.
"""

# TODO: BaseHTTPException(HTTPException) и наследники.
