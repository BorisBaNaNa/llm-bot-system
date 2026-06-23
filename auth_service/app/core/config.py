"""Конфигурация Auth Service (env -> Settings).

Через pydantic-settings читаются переменные окружения и собирается единый
объект settings: APP_NAME, ENV, JWT_SECRET, JWT_ALG, ACCESS_TOKEN_EXPIRE_MINUTES,
путь к БД (SQLITE_PATH / DATABASE_URL). Только конфигурация, без запуска
приложения и без запросов к БД.
"""

# TODO: class Settings(BaseSettings) и settings = Settings().
