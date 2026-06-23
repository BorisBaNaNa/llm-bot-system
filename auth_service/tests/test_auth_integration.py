"""Интеграционные тесты Auth Service через HTTP (httpx ASGITransport).

Полный поток: register -> login (form-data, OAuth2PasswordRequestForm) -> me
(с Authorization: Bearer). Негативные: повторный register -> 409, неверный
пароль -> 401, /auth/me без/с неверным токеном -> 401.
"""

# TODO: test_register_login_me_flow, test_duplicate_409, test_bad_password_401,
#       test_me_without_token_401.
