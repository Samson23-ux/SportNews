import pytest
from httpx import Response, AsyncClient


from tests.integration_tests.fake_data import fake_user
from tests.integration_tests.database import (
    async_client,
    initialize_db,
    get_test_session,
)


@pytest.mark.asyncio
async def test_get_user_profile(async_client: AsyncClient, create_user: Response):
    user_email: str = fake_user.email
    user_password: str = fake_user.password

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": user_email, "password": user_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    res = await async_client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    json_res = res.json()

    assert res.status_code == 200
    assert user_email == json_res["data"]["email"]


@pytest.mark.asyncio
async def test_get_user_profile_settings(async_client: AsyncClient, create_user: Response):
    user_email: str = fake_user.email
    user_password: str = fake_user.password

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": user_email, "password": user_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    res = await async_client.get(
        "/api/v1/users/me/settings",
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    json_res = res.json()

    assert res.status_code == 200
    assert "theme" in json_res["data"]


@pytest.mark.asyncio
async def test_update_user_profile_settings(async_client: AsyncClient, create_user: Response):
    user_email: str = fake_user.email
    user_password: str = fake_user.password

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": user_email, "password": user_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]
    settings_update: dict = {"theme": "dark"}

    res = await async_client.patch(
        "/api/v1/users/me/settings",
        json=settings_update,
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    json_res = res.json()
    theme: str = settings_update.get("theme")

    assert res.status_code == 200
    assert theme == json_res["data"]["theme"]
