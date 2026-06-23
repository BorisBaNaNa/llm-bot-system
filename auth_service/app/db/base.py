"""Базовый класс SQLAlchemy для моделей Auth Service.

Единый источник Base (DeclarativeBase) для всех ORM-моделей. Только базовая
декларация, без самих моделей.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Общий предок всех ORM-моделей; хранит реестр таблиц (metadata)."""
