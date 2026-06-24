"""Фикстуры тестов Bot Service.

Готовят тестовую инфраструктуру: Redis через fakeredis и патч get_redis именно
там, где он используется (app.bot.handlers.get_redis), чтобы тесты не пытались
подключиться к реальному redis:6379.
"""

import pytest
from fakeredis import aioredis


@pytest.fixture
def fake_redis(monkeypatch):
    """Поднять in-memory Redis и подсунуть его хэндлерам вместо реального.

    Патчим именно app.bot.handlers.get_redis - точку, где хэндлеры берут клиент.
    decode_responses=True повторяет поведение настоящего get_redis (строки, не bytes).
    """
    redis = aioredis.FakeRedis(decode_responses=True)
    monkeypatch.setattr("app.bot.handlers.get_redis", lambda: redis)
    return redis
