import pytest
from httpx import Response, AsyncClient


from tests.fake_data import fake_editor


@pytest.mark.asyncio
async def test_get_editor_articles(create_article: Response, async_client: AsyncClient):
    editor_email: str = fake_editor.get("email")
    editor_password: str = fake_editor.get("password")

    article_json_res = create_article.json()
    article_id: str = article_json_res["data"]["id"]

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": editor_email, "password": editor_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]
    article_update: dict = {"title": "new_fake_title"}

    await async_client.patch(
        f"/api/v1/articles/{article_id}",
        json=article_update,
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    res = await async_client.get(
        "/api/v1/editors/me/articles",
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    json_res = res.json()

    assert res.status_code == 200
    assert len(json_res["data"]) >= 1


@pytest.mark.asyncio
async def test_get_editor_dashboard(create_article: Response, async_client: AsyncClient):
    editor_email: str = fake_editor.get("email")
    editor_password: str = fake_editor.get("password")

    article_json_res = create_article.json()
    article_id: str = article_json_res["data"]["id"]

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": editor_email, "password": editor_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]
    article_update: dict = {"title": "new_fake_title"}

    await async_client.patch(
        f"/api/v1/articles/{article_id}",
        json=article_update,
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    res = await async_client.get(
        "/api/v1/editors/me/analytics/dashboard",
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    json_res = res.json()
    total_articles: int = json_res["data"]["total_articles"]

    assert res.status_code == 200
    assert total_articles == 1


@pytest.mark.asyncio
async def test_get_editor_profile(
    create_editor: Response, async_client: AsyncClient
):
    editor_email: str = fake_editor.get("email")
    editor_password: str = fake_editor.get("password")

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": editor_email, "password": editor_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    res = await async_client.get(
        "/api/v1/editors/me",
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    json_res = res.json()
    editor_name: str = fake_editor.get("name")

    assert res.status_code == 200
    assert editor_name == json_res["data"]["name"]


@pytest.mark.asyncio
async def test_get_editor_settings(
    create_editor: Response, async_client: AsyncClient
):
    editor_email: str = fake_editor.get("email")
    editor_password: str = fake_editor.get("password")

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": editor_email, "password": editor_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    res = await async_client.get(
        "/api/v1/editors/me/settings",
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    json_res = res.json()

    assert res.status_code == 200
    assert "theme" in json_res["data"]


@pytest.mark.asyncio
async def test_update_editor_settings(
    create_editor: Response, async_client: AsyncClient
):
    editor_email: str = fake_editor.get("email")
    editor_password: str = fake_editor.get("password")

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": editor_email, "password": editor_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]
    settings_update: dict = {"auto_delete_drafts": True}

    res = await async_client.patch(
        "/api/v1/writers/me/settings",
        json=settings_update,
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    json_res = res.json()
    auto_delete_drafts: bool = json_res["data"]["auto_delete_drafts"]

    assert res.status_code == 200
    assert auto_delete_drafts
