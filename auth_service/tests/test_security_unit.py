"""Модульные тесты функций безопасности (чистые функции, без БД и FastAPI).

Проверяют: хеш не равен паролю, verify проходит на верном и не проходит на
неверном; create_access_token + decode_token дают payload с sub/role/iat/exp,
и sub/role совпадают с переданными.
"""

# TODO: test_hash_password, test_verify_password, test_jwt_roundtrip.
