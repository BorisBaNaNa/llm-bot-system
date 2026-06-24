"""Сборка aiogram: Bot и Dispatcher.

Создаются Bot и Dispatcher, подключаются роутеры/handlers. Без бизнес-логики
проверки токена и запроса к LLM - только сборка и регистрация обработчиков.
"""

import asyncio

from aiogram import Bot, Dispatcher

from app.bot.handlers import router
from app.core.config import settings


def create_bot() -> Bot:
    """Создать Bot с токеном из настроек.

    Фабрика, а не объект на уровне модуля: aiogram валидирует токен при создании,
    и пустой токен в тестах/линтере не должен валить импорт модуля.
    """
    return Bot(token=settings.telegram_bot_token)


def create_dispatcher() -> Dispatcher:
    """Создать Dispatcher и подключить обработчики."""
    dp = Dispatcher()
    dp.include_router(router)
    return dp


async def run_polling() -> None:
    """Запустить бота в режиме long polling (отдельный процесс)."""
    bot = create_bot()
    dp = create_dispatcher()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(run_polling())
