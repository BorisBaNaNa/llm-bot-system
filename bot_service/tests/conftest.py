"""Фикстуры тестов Bot Service.

Готовят тестовую инфраструктуру: Redis через fakeredis и патч get_redis именно
там, где он используется (app.bot.handlers.get_redis), чтобы тесты не пытались
подключиться к реальному redis:6379.
"""

# TODO: фикстура fake_redis и патч app.bot.handlers.get_redis.
