"""Мок-тесты обработчиков Telegram (fakeredis + pytest-mock).

/token <jwt>: токен сохраняется в fake redis под ключом token:<tg_user_id>.
Обычный текст без токена: Celery не вызывается, бот отвечает об отсутствии токена.
Обычный текст с токеном: вызывается llm_request.delay(...) с верными аргументами
(delay мокается), пользователю уходит "Запрос принят".
"""

from unittest.mock import AsyncMock, MagicMock

from jose import jwt

from app.bot import handlers
from app.core.config import settings


def _make_message(text: str, user_id: int, chat_id: int) -> MagicMock:
    """Собрать фейковое Telegram-сообщение с async-методом answer."""
    message = MagicMock()
    message.from_user.id = user_id
    message.chat.id = chat_id
    message.text = text
    message.answer = AsyncMock()
    return message


def _make_command(args: str | None) -> MagicMock:
    """Фейковый CommandObject - у него хэндлер /token читает args."""
    command = MagicMock()
    command.args = args
    return command


def _valid_token(sub: str) -> str:
    """Токен на том же секрете, что проверяет бот (как будто выдал auth)."""
    return jwt.encode(
        {"sub": sub, "role": "user"},
        settings.jwt_secret,
        algorithm=settings.jwt_alg,
    )


async def test_token_saved(fake_redis):
    """/token с валидным токеном сохраняет его в Redis под token:<id>."""
    token = _valid_token(sub="100")
    message = _make_message(f"/token {token}", user_id=100, chat_id=100)

    await handlers.cmd_token(message, _make_command(token))

    assert await fake_redis.get("token:100") == token
    message.answer.assert_awaited()


async def test_no_token_no_celery(fake_redis, mocker):
    """Текст без сохранённого токена не ставит задачу и просит авторизоваться."""
    delay = mocker.patch.object(handlers.llm_request, "delay")
    message = _make_message("привет", user_id=200, chat_id=200)

    await handlers.handle_text(message)

    delay.assert_not_called()
    message.answer.assert_awaited()


async def test_text_calls_celery(fake_redis, mocker):
    """Текст с валидным токеном публикует llm_request.delay с chat_id и текстом."""
    await fake_redis.set("token:300", _valid_token(sub="300"))
    delay = mocker.patch.object(handlers.llm_request, "delay")
    message = _make_message("сколько будет 2+2", user_id=300, chat_id=999)

    await handlers.handle_text(message)

    delay.assert_called_once_with(999, "сколько будет 2+2")
    message.answer.assert_awaited()
