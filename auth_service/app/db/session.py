"""Асинхронный engine и фабрика сессий Auth Service.

Строка подключения собирается из настроек, создаётся create_async_engine(...) и
AsyncSessionLocal (async_sessionmaker). Файл не открывает сессию сам - он даёт
инструменты для открытия сессии через dependencies.
"""

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import settings

# sqlite — СУБД, aiosqlite — асинхронный драйвер; путь к файлу из настроек.
DATABASE_URL = f"sqlite+aiosqlite:///{settings.sqlite_path}"

# Один движок на всё приложение (пул соединений).
engine = create_async_engine(DATABASE_URL, echo=False)

# Фабрика сессий: на каждый запрос берём свежую сессию.
# expire_on_commit=False — объекты остаются читаемыми после commit (важно в async).
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
)
