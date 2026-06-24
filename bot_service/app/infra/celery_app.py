"""Объект Celery приложения.

celery_app с правильными broker (RabbitMQ) и backend (Redis). Обязательно
регистрируются задачи: autodiscover_tasks(["app.tasks"]) либо явный импорт
app.tasks.llm_tasks, чтобы задача llm_request не падала с KeyError. Кода бота тут
нет.
"""

from celery import Celery

from app.core.config import settings

# broker - RabbitMQ (куда кладём задачи), backend - Redis (где забираем результат).
# include импортирует модуль задач при старте воркера: так llm_request попадает в
# реестр и не падает с KeyError, а циклического импорта при создании приложения нет
# (llm_tasks сам импортирует celery_app).
celery_app = Celery(
    "bot_service",
    broker=settings.rabbitmq_url,
    backend=settings.redis_url,
    include=["app.tasks.llm_tasks"],
)
