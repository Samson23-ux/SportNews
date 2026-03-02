import pytest
from httpx import Response, AsyncClient


from tests.fake_data import fake_author, fake_user


@pytest.mark.asyncio
async def test_get_author_articles(create_article: Response, async_client: AsyncClient):
    author_email: str = fake_author.get("email")
    author_password: str = fake_author.get("password")

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": author_email, "password": author_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    res = await async_client.get(
        "/api/v1/authors/me/articles",
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    json_res = res.json()

    assert res.status_code == 200
    assert len(json_res["data"]) >= 1


@pytest.mark.asyncio
async def test_get_author_dashboard(create_article: Response, async_client: AsyncClient):
    author_email: str = fake_author.get("email")
    author_password: str = fake_author.get("password")

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": author_email, "password": author_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    res = await async_client.get(
        "/api/v1/authors/me/analytics/dashboard",
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    json_res = res.json()
    total_articles: int = json_res["data"]["total_articles"]

    assert res.status_code == 200
    assert total_articles == 1


@pytest.mark.asyncio
async def test_get_author_profile(create_author: Response, async_client: AsyncClient):
    author_email: str = fake_author.get("email")
    author_password: str = fake_author.get("password")

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": author_email, "password": author_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    res = await async_client.get(
        "/api/v1/authors/me",
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    json_res = res.json()
    author_name: str = fake_author.get("name")

    assert res.status_code == 200
    assert author_name == json_res["data"]["name"]


@pytest.mark.asyncio
async def test_unauthorized_get_author_profile(
    create_author: Response, async_client: AsyncClient
):
    user_email: str = fake_user.get("email")
    user_password: str = fake_user.get("password")

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": user_email, "password": user_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    res = await async_client.get(
        "/api/v1/authors/me",
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    assert res.status_code == 403


@pytest.mark.asyncio
async def test_unauthenticated_get_author_profile(
    create_author: Response, async_client: AsyncClient
):
    res = await async_client.get("/api/v1/authors/me")

    assert res.status_code == 401


@pytest.mark.asyncio
async def test_get_author_settings(
    async_client: AsyncClient, create_author: Response
):
    author_email: str = fake_author.get("email")
    author_password: str = fake_author.get("password")

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": author_email, "password": author_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    res = await async_client.get(
        "/api/v1/authors/me/settings",
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    json_res = res.json()

    assert res.status_code == 200
    assert "theme" in json_res["data"]


@pytest.mark.asyncio
async def test_update_author_settings(
    async_client: AsyncClient, create_author: Response
):
    author_email: str = fake_author.get("email")
    author_password: str = fake_author.get("password")

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": author_email, "password": author_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]
    settings_update: dict = {"auto_delete_drafts": True}

    res = await async_client.patch(
        "/api/v1/authors/me/settings",
        json=settings_update,
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    json_res = res.json()

    assert res.status_code == 200
    assert json_res["data"]["theme"] is True
