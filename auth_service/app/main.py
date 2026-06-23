"""Точка входа Auth Service (FastAPI).

Сборка приложения как композиции: подключение роутеров, обработчиков
исключений, lifespan и системных ручек (например /health). Без бизнес-логики
и без SQL.
"""

from fastapi import FastAPI


def create_app() -> FastAPI:
    """Собрать и сконфигурировать приложение FastAPI."""
    app = FastAPI(title="auth-service")

    # TODO: lifespan для создания таблиц (Base.metadata.create_all).
    # TODO: подключить роутеры (api.router) и обработчики исключений.

    @app.get("/health", tags=["health"])
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
