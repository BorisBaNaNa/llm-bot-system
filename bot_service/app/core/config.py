"""Конфигурация Bot Service (env -> Settings).

Через pydantic-settings собирается settings: TELEGRAM_BOT_TOKEN, JWT_SECRET,
JWT_ALG, REDIS_URL, RABBITMQ_URL, настройки OpenRouter. Для docker-compose
значения по умолчанию - хосты redis и rabbitmq, а не localhost.
"""

# TODO: class Settings(BaseSettings) и settings = Settings().
