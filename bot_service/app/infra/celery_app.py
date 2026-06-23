"""Объект Celery приложения.

celery_app с правильными broker (RabbitMQ) и backend (Redis). Обязательно
регистрируются задачи: autodiscover_tasks(["app.tasks"]) либо явный импорт
app.tasks.llm_tasks, чтобы задача llm_request не падала с KeyError. Кода бота тут
нет.
"""

# TODO: celery_app = Celery(...); broker/backend; регистрация tasks.
