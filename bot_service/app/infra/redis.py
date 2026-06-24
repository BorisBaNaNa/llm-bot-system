"""Единая точка доступа к Redis.

get_redis() возвращает redis.asyncio.Redis на основе settings.redis_url.
Не создавать новый клиент на каждый вызов без необходимости. В тестах этот слой
мокается (fakeredis), патчится там, где используется (app.bot.handlers.get_redis).
"""

from redis.asyncio import Redis

from app.core.config import settings

# Ленивый синглтон: один клиент на процесс. Redis сам держит пул соединений,
# плодить новые клиенты на каждый вызов незачем.
_redis: Redis | None = None


def get_redis() -> Redis:
    """Вернуть общий async-клиент Redis (создаётся при первом обращении).

    decode_responses=True - чтобы из Redis приходили str, а не bytes: токены и
    тексты удобнее читать строками. В тестах эта функция патчится на fakeredis,
    поэтому реального подключения там не происходит.
    """
    global _redis
    if _redis is None:
        _redis = Redis.from_url(settings.redis_url, decode_responses=True)
    return _redis
