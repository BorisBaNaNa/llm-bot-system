"""Pydantic-схемы регистрации и токенов.

RegisterRequest (email + password), TokenResponse (access_token + token_type).
При желании LoginResponse. Для /auth/login используется OAuth2PasswordRequestForm,
поэтому отдельная схема входа для логина может не требоваться.
"""

# TODO: RegisterRequest, TokenResponse.
