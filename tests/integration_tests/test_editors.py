import pytest
from httpx import Response, AsyncClient


from tests.integration_tests.fake_data import fake_editor, fake_admin
from tests.integration_tests.database import (
    async_client,
    initialize_db,
    get_test_session,
)


@pytest.mark.asyncio
async def test_get_editor_articles(create_article: Response, async_client: AsyncClient):
    editor_email: str = fake_editor.email
    editor_password: str = fake_editor.password

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
    editor_email: str = fake_editor.email
    editor_password: str = fake_editor.password

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
    editor_email: str = fake_editor.email
    editor_password: str = fake_editor.password

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
    editor_name: str = fake_editor.name

    assert res.status_code == 200
    assert editor_name == json_res["data"]["name"]


@pytest.mark.asyncio
async def test_get_editor_settings(
    create_editor: Response, async_client: AsyncClient
):
    editor_email: str = fake_editor.email
    editor_password: str = fake_editor.password

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
async def test_mark_article_edited(
    create_article: Response, create_editor: Response, async_client: AsyncClient
):
    admin_email: str = fake_admin.email
    admin_password: str = fake_admin.password

    editor_name: str = fake_editor.name
    editor_email: str = fake_editor.email
    editor_password: str = fake_editor.password

    article_json = create_article.json()
    editor_json = create_editor.json()

    article_id: str = article_json["data"]["id"]
    editor_id: str = editor_json["data"]["id"]

    admin_sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": admin_email, "password": admin_password},
        headers={"curr_env": "testing"},
    )

    admin_access_token: str = admin_sign_in_res.json()["access_token"]

    editor_sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": editor_email, "password": editor_password},
        headers={"curr_env": "testing"},
    )

    editor_access_token: str = editor_sign_in_res.json()["access_token"]

    # assign article to editor
    await async_client.post(
        f"/admin/editors/{editor_id}/articles/{article_id}/assign",
        headers={"Authorization": f"Bearer {admin_access_token}", "curr_env": "testing"},
    )

    res = await async_client.patch(
        f"/editors/articles/{article_id}/edited",
        headers={"Authorization": f"Bearer {editor_access_token}", "curr_env": "testing"},
    )

    json_res = res.json()

    assert res.status_code == 201
    assert editor_name == json_res["data"]["editor"]



@pytest.mark.asyncio
async def test_update_editor_settings(
    create_editor: Response, async_client: AsyncClient
):
    editor_email: str = fake_editor.email
    editor_password: str = fake_editor.password

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
