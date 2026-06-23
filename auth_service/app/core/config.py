"""Конфигурация Auth Service (env -> Settings).

Через pydantic-settings читаются переменные окружения и собирается единый
объект settings: APP_NAME, ENV, JWT_SECRET, JWT_ALG, ACCESS_TOKEN_EXPIRE_MINUTES,
путь к БД (SQLITE_PATH / DATABASE_URL). Только конфигурация, без запуска
приложения и без запросов к БД.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки сервиса, считанные из переменных окружения / .env."""

    # Откуда и как читать настройки.
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # лишние переменные в .env не валят запуск
    )

    # --- Приложение ---
    app_name: str = "auth-service"
    env: str = "local"

    # --- JWT ---
    # Секрет общий с bot_service: бот проверяет токены, выданные этим сервисом.
    jwt_secret: str
    jwt_alg: str = "HS256"
    access_token_expire_minutes: int = 60

    # --- База данных ---
    sqlite_path: str = "./auth.db"


# Единственный экземпляр: .env читается один раз, остальной код импортирует его.
settings = Settings()
