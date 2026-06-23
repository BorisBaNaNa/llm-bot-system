"""Интеграционные тесты Auth Service через HTTP (httpx ASGITransport).

Полный поток: register -> login (form-data, OAuth2PasswordRequestForm) -> me
(с Authorization: Bearer). Негативные: повторный register -> 409, неверный
пароль -> 401, /auth/me без/с неверным токеном -> 401.
"""


async def test_register_login_me_flow(client):
    # register -> 201, в ответе нет хеша пароля
    r = await client.post(
        "/auth/register",
        json={"email": "ivanov@email.com", "password": "password123"},
    )
    assert r.status_code == 201
    body = r.json()
    assert body["email"] == "ivanov@email.com"
    assert body["role"] == "user"
    assert "password_hash" not in body

    # login -> 200, выдан bearer-токен
    r = await client.post(
        "/auth/login",
        data={"username": "ivanov@email.com", "password": "password123"},
    )
    assert r.status_code == 200
    token_data = r.json()
    assert token_data["token_type"] == "bearer"
    token = token_data["access_token"]

    # me -> 200, профиль текущего пользователя
    r = await client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json()["email"] == "ivanov@email.com"


async def test_duplicate_register_409(client):
    payload = {"email": "petrov@email.com", "password": "password123"}
    assert (await client.post("/auth/register", json=payload)).status_code == 201
    # повторная регистрация на тот же email
    assert (await client.post("/auth/register", json=payload)).status_code == 409


async def test_bad_password_401(client):
    await client.post(
        "/auth/register",
        json={"email": "sidorov@email.com", "password": "password123"},
    )
    r = await client.post(
        "/auth/login",
        data={"username": "sidorov@email.com", "password": "wrong-password"},
    )
    assert r.status_code == 401


async def test_me_without_token_401(client):
    r = await client.get("/auth/me")
    assert r.status_code == 401


async def test_me_with_bad_token_401(client):
    r = await client.get(
        "/auth/me", headers={"Authorization": "Bearer broken.token.value"}
    )
    assert r.status_code == 401
