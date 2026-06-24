"""Обработчики Telegram (aiogram).

/token <jwt>: валидирует токен и сохраняет его в Redis под ключом token:<tg_user_id>.
Обычный текст: проверяет наличие и валидность токена в Redis, затем публикует
задачу в Celery (llm_request.delay(...)) и уведомляет, что запрос принят.
Нет токена или он неверный - отказ и инструкция авторизоваться в Auth Service.
"""

from aiogram import F, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from app.core.jwt import decode_and_validate
from app.infra.redis import get_redis
from app.tasks.llm_tasks import llm_request

router = Router()


def _token_key(tg_user_id: int) -> str:
    """Ключ Redis, под которым хранится токен конкретного пользователя."""
    return f"token:{tg_user_id}"


@router.message(Command("token"))
async def cmd_token(message: Message, command: CommandObject) -> None:
    """Принять /token <jwt>: проверить токен и сохранить его в Redis.

    Бот сам токены не выпускает - он лишь убеждается, что присланный токен
    подписан общим с auth_service секретом и не истёк, и тогда запоминает его.
    """
    token = (command.args or "").strip()
    if not token:
        await message.answer("Использование: /token <jwt>")
        return

    try:
        decode_and_validate(token)
    except ValueError as exc:
        await message.answer(
            f"Токен не принят: {exc}. Получите токен в Auth Service и пришлите снова."
        )
        return

    redis = get_redis()
    await redis.set(_token_key(message.from_user.id), token)
    await message.answer("Токен сохранён. Теперь можете отправлять вопросы.")


@router.message(F.text & ~F.text.startswith("/"))
async def handle_text(message: Message) -> None:
    """Обработать обычный текст: проверить токен и поставить задачу в очередь.

    Токен достаём из Redis и проверяем заново - он мог истечь с момента /token.
    Сам в LLM не ходим: публикуем llm_request в очередь, ответ доставит воркер.
    """
    redis = get_redis()
    token = await redis.get(_token_key(message.from_user.id))
    if not token:
        await message.answer(
            "Нет токена. Авторизуйтесь в Auth Service и пришлите его командой /token <jwt>."
        )
        return

    try:
        decode_and_validate(token)
    except ValueError as exc:
        await message.answer(f"Токен невалиден: {exc}. Авторизуйтесь заново.")
        return

    llm_request.delay(message.chat.id, message.text)
    await message.answer("Запрос принят, ответ придёт чуть позже.")
