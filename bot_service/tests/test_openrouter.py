"""Интеграционные тесты клиента OpenRouter через respx (без реального интернета).

Поднимается мок-роут на POST https://openrouter.ai/api/v1/chat/completions,
возвращается JSON с choices[0].message.content. Проверяется, что call_openrouter
вернул текст и что HTTP-вызов реально был сделан.
"""

import respx
from httpx import Response

from app.services.openrouter_client import call_openrouter


@respx.mock
def test_call_openrouter_returns_text():
    """Клиент достаёт текст из choices и реально делает HTTP-запрос."""
    route = respx.post("https://openrouter.ai/api/v1/chat/completions").mock(
        return_value=Response(
            200,
            json={"choices": [{"message": {"content": "Привет из LLM"}}]},
        )
    )

    result = call_openrouter("сколько будет 2+2")

    assert result == "Привет из LLM"
    assert route.called
