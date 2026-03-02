import pytest
from httpx import Response, AsyncClient


from tests.fake_data import fake_user


@pytest.mark.asyncio
async def test_sign_up(create_user: Response):
    json_res = create_user.json()
    user_email: str = fake_user.get("email")

    assert create_user.status_code == 201
    assert "id" in json_res["data"]
    assert user_email == json_res["data"]["email"]


@pytest.mark.asyncio
async def test_sign_up_with_bad_input(async_client: AsyncClient):
    res = await async_client.post(
        "/api/v1/auth/sign-up",
        json={"email": 24442, "password": fake_user.get("password")},
        headers={"curr_env": "testing"},
    )

    assert res.status_code == 400


@pytest.mark.asyncio
async def test_resend_email_code(async_client: AsyncClient, create_user: Response):
    json_res = create_user.json()
    user_id: str = json_res["data"]["id"]

    res = await async_client.post(f"/api/v1/auth/{user_id}/resend-code")

    assert res.status_code == 201


@pytest.mark.asyncio
async def test_sign_in(async_client: AsyncClient, create_user: Response):
    user_email: str = fake_user.get("email")
    user_password: str = fake_user.get("password")

    res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": user_email, "password": user_password},
        headers={"curr_env": "testing"},
    )

    json_res = res.json()

    assert res.status_code == 201
    assert "access_token" in json_res


@pytest.mark.asyncio
async def test_create_new_token(async_client: AsyncClient, create_user: Response):
    user_email: str = fake_user.get("email")
    user_password: str = fake_user.get("password")

    await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": user_email, "password": user_password},
        headers={"curr_env": "testing"},
    )

    res = await async_client.post(
        "/api/v1/auth/refresh",
    )

    json_res = res.json()

    assert res.status_code == 201
    assert "access_token" in json_res


@pytest.mark.asyncio
async def test_verify_account(async_client: AsyncClient, create_user: Response):
    json_res = create_user.json()
    user_id: str = json_res["data"]["id"]
    code: str = "randfakecode1552tghhs7"

    res = await async_client.patch(
        f"/api/v1/auth/{user_id}/verify/{code}"
    )

    assert res.status_code == 200


@pytest.mark.asyncio
async def test_sign_out(async_client: AsyncClient, create_user: Response):
    user_email: str = fake_user.get("email")
    user_password: str = fake_user.get("password")

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": user_email, "password": user_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    res = await async_client.patch(
        "/api/v1/auth/sign-out",
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    assert res.status_code == 200


@pytest.mark.asyncio
async def test_update_password(async_client: AsyncClient, create_user: Response):
    user_email: str = fake_user.get("email")
    user_password: str = fake_user.get("password")

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": user_email, "password": user_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]
    new_password: str = "fake_new_password"

    res = await async_client.patch(
        "/api/v1/auth/password-update",
        json={"curr_password": user_password, "new_password": new_password},
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    assert res.status_code == 200

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": user_email, "password": user_password},
        headers={"curr_env": "testing"},
    )

    json_res = res.json()

    assert sign_in_res.status_code == 201
    assert "access_token" in json_res


@pytest.mark.asyncio
async def test_unauthenticated_user(async_client: AsyncClient, create_user: Response):
    user_password: str = fake_user.get("password")
    new_password: str = "fake_new_password"

    res = await async_client.patch(
        "/api/v1/auth/password-update",
        json={"curr_password": user_password, "new_password": new_password},
        headers={"curr_env": "testing"},
    )

    assert res.status_code == 401


@pytest.mark.asyncio
async def test_reset_password(async_client: AsyncClient, create_user: Response):
    user_email: str = fake_user.get("email")
    new_password: str = "fake_new_password"

    res = await async_client.patch(
        "/api/v1/auth/reset-password",
        data={"email": user_email, "password": new_password},
        headers={"curr_env": "testing"},
    )

    assert res.status_code == 200

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": user_email, "password": new_password},
        headers={"curr_env": "testing"},
    )

    json_res = res.json()

    assert sign_in_res.status_code == 201
    assert "access_token" in json_res


@pytest.mark.asyncio
async def test_user_not_found(async_client: AsyncClient, create_user: Response):
    user_email: str = fake_user.get("randomuser@example.com")
    new_password: str = "fake_new_password"

    res = await async_client.patch(
        "/api/v1/auth/reset-password",
        data={"email": user_email, "password": new_password},
        headers={"curr_env": "testing"},
    )

    assert res.status_code == 404


@pytest.mark.asyncio
async def test_delete_user(async_client: AsyncClient, create_user: Response):
    user_email: str = fake_user.get("email")
    user_password: str = fake_user.get("password")

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": user_email, "password": user_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    res = await async_client.request(
        "DELETE",
        "/api/v1/auth",
        data={"password": user_password},
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    assert res.status_code == 204

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": user_email, "password": user_password},
        headers={"curr_env": "testing"},
    )

    assert sign_in_res.status_code == 404
