"""Сборка aiogram: Bot и Dispatcher.

Создаются Bot и Dispatcher, подключаются роутеры/handlers. Без бизнес-логики
проверки токена и запроса к LLM - только сборка и регистрация обработчиков.
"""

# TODO: bot = Bot(...); dp = Dispatcher(); dp.include_router(handlers.router).
