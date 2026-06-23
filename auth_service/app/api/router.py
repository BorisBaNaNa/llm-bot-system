"""Сборка роутеров Auth Service.

Создаётся общий APIRouter, к нему подключается routes_auth.router; итоговый
роутер включается в main.py. Удобно, когда роутеров становится много.
"""

from fastapi import APIRouter

from app.api import routes_auth

api_router = APIRouter()
api_router.include_router(routes_auth.router)
