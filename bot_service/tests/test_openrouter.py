"""Интеграционные тесты клиента OpenRouter через respx (без реального интернета).

Поднимается мок-роут на POST https://openrouter.ai/api/v1/chat/completions,
возвращается JSON с choices[0].message.content. Проверяется, что call_openrouter
вернул текст и что HTTP-вызов реально был сделан.
"""

# TODO: test_call_openrouter_returns_text (respx mock).
