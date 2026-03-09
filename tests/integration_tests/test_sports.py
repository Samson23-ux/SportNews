import pytest
from httpx import Response, AsyncClient


from tests.fake_data import fake_user
from tests.integration_tests.database import (
    async_client,
    initialize_db,
    get_test_session,
)


@pytest.mark.asyncio
async def test_get_all_sports(async_client: AsyncClient, create_user: Response):
    user_email: str = fake_user.email
    user_password: str = fake_user.password

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": user_email, "password": user_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    res = await async_client.get(
        "/sports",
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    json_res = res.json()

    assert res.status_code == 200
    assert len(json_res["data"]) >= 1


@pytest.mark.asyncio
async def test_get_sports_teams(async_client: AsyncClient, create_user: Response):
    user_email: str = fake_user.email
    user_password: str = fake_user.password

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": user_email, "password": user_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    res = await async_client.get(
        "/sports/golf/teams",
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    json_res = res.json()

    assert res.status_code == 200
    assert len(json_res["data"]) >= 1


@pytest.mark.asyncio
async def test_get_sports_competition(async_client: AsyncClient, create_user: Response):
    user_email: str = fake_user.email
    user_password: str = fake_user.password

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": user_email, "password": user_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    res = await async_client.get(
        "/sports/golf/competitions",
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    json_res = res.json()

    assert res.status_code == 200
    assert len(json_res["data"]) >= 1
