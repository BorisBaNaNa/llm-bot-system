"""Celery-задача llm_request.

Получает tg_chat_id и prompt, вызывает OpenRouter через клиент, формирует ответ
и доставляет его пользователю (отправка из воркера либо сохранение результата в
Redis для последующей отправки ботом).
"""

# TODO: @celery_app.task(name="llm_request") def llm_request(tg_chat_id, prompt): ...
