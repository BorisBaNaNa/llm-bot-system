# llm-bot-system

Распределённая система LLM-консультаций из двух независимых сервисов.

- **auth_service** - сервис аутентификации на FastAPI: регистрация, логин, выпуск JWT.
- **bot_service** - Telegram-бот на aiogram: валидирует JWT (но не создаёт его) и
  через очередь Celery + RabbitMQ обращается к LLM (OpenRouter), Redis хранит токены и
  результаты.

Это итоговый учебный проект. Подробное описание архитектуры, запуск и скриншоты будут
добавлены по мере реализации.

## Структура

```
llm-bot-system/
├── auth_service/   # FastAPI + JWT + SQLite
└── bot_service/    # aiogram + Celery + RabbitMQ + Redis + OpenRouter
```

Каждый сервис - самостоятельный проект со своим pyproject.toml, .env и тестами.
