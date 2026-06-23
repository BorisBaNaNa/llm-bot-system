"""Обработчики Telegram (aiogram).

/token <jwt>: валидирует токен и сохраняет его в Redis под ключом token:<tg_user_id>.
Обычный текст: проверяет наличие и валидность токена в Redis, затем публикует
задачу в Celery (llm_request.delay(...)) и уведомляет, что запрос принят.
Нет токена или он неверный - отказ и инструкция авторизоваться в Auth Service.
"""

# TODO: router; handler /token; handler текста (проверка токена -> llm_request.delay).
