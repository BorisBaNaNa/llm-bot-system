"""Эндпоинты Auth Service (/auth/*).

Тонкие маршруты: принимают вход, вызывают usecase, возвращают результат.
Без SQL и без прямой генерации токенов. Маршруты: /auth/register, /auth/login
(через OAuth2PasswordRequestForm = Depends()), /auth/me.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])

# TODO: register, login, me.
