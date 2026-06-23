"""Функции безопасности Auth Service.

bcrypt через passlib: hash_password() и verify_password().
JWT через python-jose: create_access_token() (payload с sub, role, iat, exp) и
decode_token() (валидация подписи и срока). Используются как строительные блоки
в usecases и deps. Без БД и без знания про роуты.
"""

# TODO: hash_password / verify_password.
# TODO: create_access_token / decode_token.
