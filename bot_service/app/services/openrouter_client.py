"""Клиент OpenRouter (httpx).

Формирует payload для /chat/completions, выставляет заголовки и модель,
отправляет запрос и возвращает текст ответа. Обязательно обрабатывает ошибки
сети и ответы не-200, чтобы воркер не падал без понятного сообщения.
"""

import httpx

from app.core.config import settings


def call_openrouter(prompt: str) -> str:
    """Спросить LLM через OpenRouter и вернуть текст ответа.

    Клиент синхронный: его зовёт Celery-воркер, которому не нужен event loop.
    Любую сетевую ошибку, не-200 или неожиданный формат ответа превращаем в
    RuntimeError с понятным текстом - воркер не должен падать молча.
    """
    url = f"{settings.openrouter_base_url}/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.openrouter_api_key}",
        "HTTP-Referer": settings.openrouter_site_url,
        "X-Title": settings.openrouter_app_name,
    }
    payload = {
        "model": settings.openrouter_model,
        "messages": [{"role": "user", "content": prompt}],
    }

    try:
        with httpx.Client(timeout=60.0) as client:
            response = client.post(url, json=payload, headers=headers)
    except httpx.HTTPError as exc:
        raise RuntimeError(f"Сеть OpenRouter недоступна: {exc}") from exc

    if response.status_code != 200:
        raise RuntimeError(
            f"OpenRouter вернул {response.status_code}: {response.text}"
        )

    try:
        return response.json()["choices"][0]["message"]["content"]
    except (KeyError, IndexError, ValueError) as exc:
        raise RuntimeError(f"Неожиданный ответ OpenRouter: {exc}") from exc
