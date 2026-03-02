import pytest
from httpx import Response, AsyncClient


from tests.fake_data import fake_user, fake_admin


@pytest.mark.asyncio
async def test_get_admin_dashboard(create_article: Response, async_client: AsyncClient):
    author_email: str = fake_admin.get("email")
    author_password: str = fake_admin.get("password")

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": author_email, "password": author_password},
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
async def test_get_all_users(create_user: Response, async_client: AsyncClient):
    admin_email: str = fake_admin.get("email")
    admin_password: str = fake_admin.get("password")

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
    admin_email: str = fake_admin.get("email")
    admin_password: str = fake_admin.get("password")

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
    admin_email: str = fake_admin.get("email")
    admin_password: str = fake_admin.get("password")

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
    admin_email: str = fake_admin.get("email")
    admin_password: str = fake_admin.get("password")

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
    admin_email: str = fake_admin.get("email")
    admin_password: str = fake_admin.get("password")

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
    admin_email: str = fake_admin.get("email")
    admin_password: str = fake_admin.get("password")

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
    admin_email: str = fake_admin.get("email")
    admin_password: str = fake_admin.get("password")

    article_json_res = create_article.json()
    article_id: str = article_json_res["data"]["id"]

    admin_sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": admin_email, "password": admin_password},
        headers={"curr_env": "testing"},
    )

    admin_access_token: str = admin_sign_in_res.json()["access_token"]

    user_email: str = fake_user.get("email")
    user_password: str = fake_user.get("password")

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
async def test_send_information(create_user: Response, async_client: AsyncClient):
    admin_email: str = fake_admin.get("email")
    admin_password: str = fake_admin.get("password")

    admin_sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": admin_email, "password": admin_password},
        headers={"curr_env": "testing"},
    )

    admin_access_token: str = admin_sign_in_res.json()["access_token"]

    user_email: str = fake_user.get("email")
    user_password: str = fake_user.get("password")

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
        headers={"Authorization": f"Bearer {admin_access_token}", "curr_env": "testing"},
    )

    assert res.status_code == 200


@pytest.mark.asyncio
async def test_send_newsletter(create_user: Response, async_client: AsyncClient):
    admin_email: str = fake_admin.get("email")
    admin_password: str = fake_admin.get("password")

    admin_sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": admin_email, "password": admin_password},
        headers={"curr_env": "testing"},
    )

    admin_access_token: str = admin_sign_in_res.json()["access_token"]

    user_email: str = fake_user.get("email")
    user_password: str = fake_user.get("password")

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
        headers={"Authorization": f"Bearer {admin_access_token}", "curr_env": "testing"},
    )

    assert res.status_code == 200


@pytest.mark.asyncio
async def test_delete_author(create_author: Response, async_client: AsyncClient):
    admin_email: str = fake_admin.get("email")
    admin_password: str = fake_admin.get("password")

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
    admin_email: str = fake_admin.get("email")
    admin_password: str = fake_admin.get("password")

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
