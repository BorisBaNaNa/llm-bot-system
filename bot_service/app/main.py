"""Точка входа Bot Service.

Создаётся FastAPI-приложение со служебными ручками (например /health). Сам бот
(aiogram) и Celery-воркер запускаются как отдельные процессы. Здесь нет логики
общения с LLM и нет прямой работы с Redis.
"""

from fastapi import FastAPI


def create_app() -> FastAPI:
    """Собрать служебное приложение Bot Service."""
    app = FastAPI(title="bot-service")

    @app.get("/health", tags=["health"])
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
