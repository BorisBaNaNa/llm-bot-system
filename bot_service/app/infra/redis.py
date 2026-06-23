"""Единая точка доступа к Redis.

get_redis() возвращает redis.asyncio.Redis на основе settings.redis_url.
Не создавать новый клиент на каждый вызов без необходимости. В тестах этот слой
мокается (fakeredis), патчится там, где используется (app.bot.handlers.get_redis).
"""

# TODO: get_redis() -> redis.asyncio.Redis.
