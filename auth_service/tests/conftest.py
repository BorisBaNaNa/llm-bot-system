"""Фикстуры тестов Auth Service.

Здесь готовится тестовая инфраструктура: приложение FastAPI с подменой
зависимости get_db на in-memory SQLite и httpx AsyncClient через ASGITransport
для интеграционных тестов.
"""

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

import app.db.models  # noqa: F401  -- регистрирует модель User в Base.metadata
from app.api.deps import get_db
from app.db.base import Base
from app.main import create_app


@pytest_asyncio.fixture
async def client():
    """HTTP-клиент к приложению поверх свежей in-memory БД на каждый тест."""
    # StaticPool + одно соединение: все сессии видят одну и ту же in-memory БД.
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    test_session = async_sessionmaker(engine, expire_on_commit=False)

    async def override_get_db():
        async with test_session() as session:
            yield session

    app = create_app()
    app.dependency_overrides[get_db] = override_get_db

    # ASGITransport зовёт приложение напрямую и не запускает lifespan,
    # поэтому реальный engine из session.py не задействуется.
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    await engine.dispose()
