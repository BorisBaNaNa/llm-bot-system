"""Celery-задача llm_request.

Получает tg_chat_id и prompt, вызывает OpenRouter через клиент, формирует ответ
и доставляет его пользователю (отправка из воркера либо сохранение результата в
Redis для последующей отправки ботом).
"""

import httpx

from app.core.config import settings
from app.infra.celery_app import celery_app
from app.services.openrouter_client import call_openrouter


def _send_to_telegram(tg_chat_id: int, text: str) -> None:
    """Отправить текст пользователю напрямую через Telegram Bot API.

    Воркер синхронный, поэтому шлём обычным httpx без aiogram и event loop.
    """
    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
    httpx.post(url, json={"chat_id": tg_chat_id, "text": text}, timeout=30.0)


@celery_app.task(name="llm_request")
def llm_request(tg_chat_id: int, prompt: str) -> str:
    """Спросить LLM и доставить ответ пользователю в Telegram.

    Задачу публикует бот через llm_request.delay(...), а исполняет Celery-воркер.
    Ошибку OpenRouter не роняем как падение задачи, а превращаем в текст для
    пользователя - иначе он остался бы без ответа. Возвращаемое значение Celery
    также сохранит в Redis-backend.
    """
    try:
        answer = call_openrouter(prompt)
    except RuntimeError as exc:
        answer = f"Ошибка LLM: {exc}"

    _send_to_telegram(tg_chat_id, answer)
    return answer
