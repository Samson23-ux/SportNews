import pytest
from httpx import Response, AsyncClient


from tests.fake_data import (
    fake_user,
    fake_admin,
    fake_author,
    fake_editor,
    fake_article,
)


@pytest.mark.asyncio
async def test_get_admin_profile_settings(async_client: AsyncClient, create_admin_user):
    admin_email: str = fake_admin.email
    admin_password: str = fake_admin.password

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": admin_email, "password": admin_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    res = await async_client.get(
        "/api/v1/admin/me/settings",
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    json_res = res.json()

    assert res.status_code == 200
    assert "theme" in json_res["data"]


@pytest.mark.asyncio
async def test_get_admin_dashboard(create_article: Response, async_client: AsyncClient):
    admin_email: str = fake_admin.email
    admin_password: str = fake_admin.password

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": admin_email, "password": admin_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    res = await async_client.get(
        "/api/v1/admin/me/analytics/dashboard",
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    json_res = res.json()
    total_articles: int = json_res["data"]["total_articles"]

    assert res.status_code == 200
    assert total_articles == 1


@pytest.mark.asyncio
async def test_get_admin_profile(async_client: AsyncClient, create_admin_user):
    admin_email: str = fake_admin.email
    admin_password: str = fake_admin.password

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": admin_email, "password": admin_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    res = await async_client.get(
        "/api/v1/admin/me",
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    json_res = res.json()

    assert res.status_code == 200
    assert admin_email == json_res["data"]["email"]


@pytest.mark.asyncio
async def test_get_all_users(create_user: Response, async_client: AsyncClient):
    admin_email: str = fake_admin.email
    admin_password: str = fake_admin.password

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": admin_email, "password": admin_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    res = await async_client.get(
        "/api/v1/admin/users",
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    json_res = res.json()

    assert res.status_code == 200
    assert len(json_res["data"]) >= 1


@pytest.mark.asyncio
async def test_users_not_found(create_admin_user, async_client: AsyncClient):
    admin_email: str = fake_admin.email
    admin_password: str = fake_admin.password

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": admin_email, "password": admin_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    res = await async_client.get(
        "/api/v1/admin/users",
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    assert res.status_code == 404


@pytest.mark.asyncio
async def test_get_all_authors(create_author: Response, async_client: AsyncClient):
    admin_email: str = fake_admin.email
    admin_password: str = fake_admin.password

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": admin_email, "password": admin_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    res = await async_client.get(
        "/api/v1/admin/authors",
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    json_res = res.json()

    assert res.status_code == 200
    assert len(json_res["data"]) >= 1


@pytest.mark.asyncio
async def test_get_all_editors(create_editor: Response, async_client: AsyncClient):
    admin_email: str = fake_admin.email
    admin_password: str = fake_admin.password

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": admin_email, "password": admin_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    res = await async_client.get(
        "/api/v1/admin/editors",
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    json_res = res.json()

    assert res.status_code == 200
    assert len(json_res["data"]) >= 1


@pytest.mark.asyncio
async def test_get_all_articles(create_article: Response, async_client: AsyncClient):
    admin_email: str = fake_admin.email
    admin_password: str = fake_admin.password

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": admin_email, "password": admin_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    res = await async_client.get(
        "/api/v1/admin/articles",
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    json_res = res.json()

    assert res.status_code == 200
    assert len(json_res["data"]) >= 1


@pytest.mark.asyncio
async def test_get_all_sports(
    create_admin_user, create_sports, async_client: AsyncClient
):
    admin_email: str = fake_admin.email
    admin_password: str = fake_admin.password

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": admin_email, "password": admin_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    res = await async_client.get(
        "/api/v1/admin/sports",
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    json_res = res.json()

    assert res.status_code == 200
    assert len(json_res["data"]) >= 1


@pytest.mark.asyncio
async def test_get_article_readers(create_article: Response, async_client: AsyncClient):
    admin_email: str = fake_admin.email
    admin_password: str = fake_admin.password

    article_json_res = create_article.json()
    article_id: str = article_json_res["data"]["id"]

    admin_sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": admin_email, "password": admin_password},
        headers={"curr_env": "testing"},
    )

    admin_access_token: str = admin_sign_in_res.json()["access_token"]

    user_email: str = fake_user.email
    user_password: str = fake_user.password

    user_sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": user_email, "password": user_password},
        headers={"curr_env": "testing"},
    )

    user_access_token: str = user_sign_in_res.json()["access_token"]

    await async_client.get(
        f"/api/v1/articles/{article_id}",
        headers={"Authorization": f"Bearer {user_access_token}", "curr_env": "testing"},
    )

    res = await async_client.get(
        "/api/v1/admin/articles",
        headers={
            "Authorization": f"Bearer {admin_access_token}",
            "curr_env": "testing",
        },
    )

    json_res = res.json()

    assert res.status_code == 200
    assert len(json_res["data"]["readers"]) >= 1


@pytest.mark.asyncio
async def test_assign_article(
    create_article: Response, create_editor: Response, async_client: AsyncClient
):
    admin_email: str = fake_admin.email
    admin_password: str = fake_admin.password

    article_title: str = fake_article.name

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

    res = await async_client.post(
        f"/admin/editors/{editor_id}/articles/{article_id}/assign",
        headers={
            "Authorization": f"Bearer {admin_access_token}",
            "curr_env": "testing",
        },
    )

    json_res = res.json()

    assert res.status_code == 201
    assert article_title == json_res["data"]["title"]


@pytest.mark.asyncio
async def test_create_author(create_author: Response):
    author_email: str = fake_author.email
    json_res = create_author.json()

    author_email == json_res["data"]["email"]


@pytest.mark.asyncio
async def test_create_editor(create_editor: Response):
    editor_email: str = fake_editor.email
    json_res = create_editor.json()

    editor_email == json_res["data"]["email"]


@pytest.mark.asyncio
async def test_send_information(create_user: Response, async_client: AsyncClient):
    admin_email: str = fake_admin.email
    admin_password: str = fake_admin.password

    admin_sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": admin_email, "password": admin_password},
        headers={"curr_env": "testing"},
    )

    admin_access_token: str = admin_sign_in_res.json()["access_token"]

    user_email: str = fake_user.email
    user_password: str = fake_user.password

    user_sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": user_email, "password": user_password},
        headers={"curr_env": "testing"},
    )

    user_access_token: str = user_sign_in_res.json()["access_token"]

    settings_update: dict = {"receive_infomation": True}

    await async_client.patch(
        "/api/v1/users/me/settings",
        json=settings_update,
        headers={"Authorization": f"Bearer {user_access_token}", "curr_env": "testing"},
    )

    res = await async_client.post(
        "/api/v1/admin/info",
        headers={
            "Authorization": f"Bearer {admin_access_token}",
            "curr_env": "testing",
        },
    )

    assert res.status_code == 200


@pytest.mark.asyncio
async def test_send_newsletter(create_user: Response, async_client: AsyncClient):
    admin_email: str = fake_admin.email
    admin_password: str = fake_admin.password

    admin_sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": admin_email, "password": admin_password},
        headers={"curr_env": "testing"},
    )

    admin_access_token: str = admin_sign_in_res.json()["access_token"]

    user_email: str = fake_user.email
    user_password: str = fake_user.password

    user_sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": user_email, "password": user_password},
        headers={"curr_env": "testing"},
    )

    user_access_token: str = user_sign_in_res.json()["access_token"]

    settings_update: dict = {"receive_newsletter": True}

    await async_client.patch(
        "/api/v1/users/me/settings",
        json=settings_update,
        headers={"Authorization": f"Bearer {user_access_token}", "curr_env": "testing"},
    )

    res = await async_client.post(
        "/api/v1/admin/newsletter",
        headers={
            "Authorization": f"Bearer {admin_access_token}",
            "curr_env": "testing",
        },
    )

    assert res.status_code == 200


@pytest.mark.asyncio
async def test_publish_article(
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
        headers={
            "Authorization": f"Bearer {admin_access_token}",
            "curr_env": "testing",
        },
    )

    # mark article edited
    await async_client.patch(
        f"/editors/articles/{article_id}/edited",
        headers={"Authorization": f"Bearer {editor_access_token}", "curr_env": "testing"},
    )

    # publish article
    res = await async_client.patch(
        f"/admin/articles/{article_id}/publish",
        headers={"Authorization": f"Bearer {admin_access_token}", "curr_env": "testing"},
    )

    json_res = res.json()

    assert res.status_code == 200
    assert editor_name == json_res["data"]["editor"]


@pytest.mark.asyncio
async def test_update_admin_profile_settings(
    async_client: AsyncClient, create_admin_user
):
    admin_email: str = fake_admin.email
    admin_password: str = fake_admin.password

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": admin_email, "password": admin_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]
    settings_update: dict = {"theme": "dark"}

    res = await async_client.patch(
        "/api/v1/admin/me/settings",
        json=settings_update,
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    json_res = res.json()
    theme: str = settings_update.get("theme")

    assert res.status_code == 200
    assert theme == json_res["data"]["theme"]


@pytest.mark.asyncio
async def test_delete_author(create_author: Response, async_client: AsyncClient):
    admin_email: str = fake_admin.email
    admin_password: str = fake_admin.password

    author_json_res = create_author.json()
    author_id: str = author_json_res["data"]["id"]

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": admin_email, "password": admin_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    res = await async_client.delete(
        f"/api/v1/admin/authors/{author_id}",
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    assert res.status_code == 204


@pytest.mark.asyncio
async def test_delete_editor(create_editor: Response, async_client: AsyncClient):
    admin_email: str = fake_admin.email
    admin_password: str = fake_admin.password

    editor_json_res = create_editor.json()
    editor_id: str = editor_json_res["data"]["id"]

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": admin_email, "password": admin_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    res = await async_client.delete(
        f"/api/v1/admin/editors/{editor_id}",
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    assert res.status_code == 204
