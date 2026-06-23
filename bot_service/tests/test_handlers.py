"""Мок-тесты обработчиков Telegram (fakeredis + pytest-mock).

/token <jwt>: токен сохраняется в fake redis под ключом token:<tg_user_id>.
Обычный текст без токена: Celery не вызывается, бот отвечает об отсутствии токена.
Обычный текст с токеном: вызывается llm_request.delay(...) с верными аргументами
(delay мокается), пользователю уходит "Запрос принят".
"""

# TODO: test_token_saved, test_no_token_no_celery, test_text_calls_celery.
