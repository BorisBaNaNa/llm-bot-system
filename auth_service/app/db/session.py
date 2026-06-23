"""Асинхронный engine и фабрика сессий Auth Service.

Строка подключения собирается из настроек, создаётся create_async_engine(...) и
AsyncSessionLocal (async_sessionmaker). Файл не открывает сессию сам - он даёт
инструменты для открытия сессии через dependencies.
"""

# TODO: engine + AsyncSessionLocal.
