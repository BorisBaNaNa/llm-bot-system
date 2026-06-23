"""Бизнес-логика Auth Service.

register(), login(), me(): проверка существования пользователя, хеширование и
проверка пароля, создание JWT, получение профиля. При ошибках бросаются
исключения из core/exceptions.py (UserAlreadyExistsError, InvalidCredentialsError,
UserNotFoundError). Без прямого SQL - только вызовы репозитория.
"""

# TODO: class AuthUseCase ...
