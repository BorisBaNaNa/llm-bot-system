"""Проверка JWT в Bot Service (только валидация, без выпуска).

decode_and_validate(token: str) -> dict: проверяет подпись и exp, возвращает
payload (с sub). При неверном или истёкшем токене бросает ValueError или
доменное исключение. Токены здесь НЕ создаются.
"""

# TODO: decode_and_validate(token).
