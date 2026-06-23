"""Фикстуры тестов Auth Service.

Здесь готовится тестовая инфраструктура: приложение FastAPI с подменой
зависимости get_db на in-memory SQLite и httpx AsyncClient через ASGITransport
для интеграционных тестов.
"""

# TODO: фикстуры app/client с in-memory SQLite и override get_db.
