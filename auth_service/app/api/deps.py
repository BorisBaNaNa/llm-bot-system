"""Зависимости FastAPI для Auth Service.

get_db() выдаёт AsyncSession; фабрики get_users_repo() и get_auth_uc();
get_current_user_id()/get_current_user() берёт токен из Authorization: Bearer,
декодирует и проверяет его, возвращает user_id/пользователя. При ошибках токена
бросает InvalidTokenError / TokenExpiredError.
"""

# TODO: get_db, get_users_repo, get_auth_uc, get_current_user_id.
