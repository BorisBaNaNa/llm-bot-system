"""Конфигурация Bot Service (env -> Settings).

Через pydantic-settings собирается settings: TELEGRAM_BOT_TOKEN, JWT_SECRET,
JWT_ALG, REDIS_URL, RABBITMQ_URL, настройки OpenRouter. Для docker-compose
значения по умолчанию - хосты redis и rabbitmq, а не localhost.
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
    app_name: str = "bot-service"
    env: str = "local"

    # --- Telegram ---
    # Реальный токен нужен только живому боту; в тестах хэндлеры дёргаются напрямую.
    telegram_bot_token: str = ""

    # --- JWT ---
    # Секрет и алгоритм ОБЯЗАНЫ совпадать с auth_service: бот лишь проверяет
    # подписи токенов, которые auth выдал, и сам токены не создаёт.
    jwt_secret: str
    jwt_alg: str = "HS256"

    # --- Инфраструктура (брокер задач и хранилище токенов/результатов) ---
    # Дефолтные хосты рассчитаны на docker-compose; для локального запуска без
    # docker заменить redis/rabbitmq на localhost в .env.
    redis_url: str = "redis://redis:6379/0"
    rabbitmq_url: str = "amqp://guest:guest@rabbitmq:5672//"

    # --- OpenRouter ---
    openrouter_api_key: str = ""
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_model: str = "stepfun/step-3.5-flash:free"
    openrouter_site_url: str = "https://example.com"
    openrouter_app_name: str = "bot-service"


# Единственный экземпляр: .env читается один раз, остальной код импортирует его.
settings = Settings()
