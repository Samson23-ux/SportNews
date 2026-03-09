import pytest
import aiofiles
from pathlib import Path
from httpx import Response, AsyncClient


from app.api.v1.schemas.articles import ImageOutV1
from tests.integration_tests.database import (
    async_client,
    initialize_db,
    get_test_session,
)
from tests.fake_data import (
    fake_user,
    fake_admin,
    fake_editor,
    fake_author,
    fake_article,
)


@pytest.mark.asyncio
async def test_get_articles(create_article: Response, async_client: AsyncClient):
    user_email: str = fake_user.email
    user_password: str = fake_user.password

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": user_email, "password": user_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    res = await async_client.get(
        "/api/v1/articles",
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    json_res = res.json()

    assert res.status_code == 200
    assert len(json_res["data"]) >= 1


@pytest.mark.asyncio
async def test_get_drafts(
    create_author: Response, async_client: AsyncClient
):
    author_email: str = fake_author.email
    author_password: str = fake_author.password

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": author_email, "password": author_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    title: str = fake_article.title
    draft_data: dict = {"title": title}

    await async_client.post(
        "/api/v1/articles/drafts",
        json=draft_data,
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    res = await async_client.get(
        "/api/v1/articles/drafts",
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    json_res = res.json()

    assert res.status_code == 200
    assert len(json_res["data"]) >= 1


@pytest.mark.asyncio
async def test_articles_not_found(create_article: Response, async_client: AsyncClient):
    user_email: str = fake_user.email
    user_password: str = fake_user.password

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": user_email, "password": user_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    res = await async_client.get(
        "/api/v1/articles?sport=boxing",
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    assert res.status_code == 404


@pytest.mark.asyncio
async def test_get_article(create_article: Response, async_client: AsyncClient):
    user_email: str = fake_user.email
    user_password: str = fake_user.password

    article_json_res = create_article.json()
    article_id: str = article_json_res["data"]["id"]
    article_title: str = fake_article.title

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": user_email, "password": user_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    res = await async_client.get(
        f"/api/v1/articles/{article_id}",
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    json_res = res.json()

    assert res.status_code == 200
    assert article_title == json_res["data"]["title"]


@pytest.mark.asyncio
async def test_get_draft(
    create_author: Response, async_client: AsyncClient
):
    author_email: str = fake_author.email
    author_password: str = fake_author.password

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": author_email, "password": author_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    title: str = fake_article.title
    draft_data: dict = {"title": title}

    draft_res = await async_client.post(
        "/api/v1/articles/drafts",
        json=draft_data,
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    draft_id: str = draft_res.json()["data"]["draft_id"]

    res = await async_client.get(
        f"/api/v1/articles/drafts/{draft_id}",
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    json_res = res.json()

    assert res.status_code == 200
    assert title == json_res["data"]["title"]


@pytest.mark.asyncio
async def test_get_article_images(create_article: Response, async_client: AsyncClient):
    user_email: str = fake_user.email
    user_password: str = fake_user.password

    article_json_res = create_article.json()
    article_id: str = article_json_res["data"]["id"]

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": user_email, "password": user_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    res = await async_client.get(
        f"/api/v1/articles/{article_id}/images",
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    assert res.status_code == 200


@pytest.mark.asyncio
async def test_create_article(create_article: Response, async_client: AsyncClient):
    json_res: Response = create_article.json()
    article_title: str = fake_article.title

    assert create_article.status_code == 201
    assert "id" in json_res["data"]
    assert article_title == json_res["data"]["title"]


@pytest.mark.asyncio
async def test_create_article_draft(
    create_author: Response, async_client: AsyncClient
):
    author_email: str = fake_author.email
    author_password: str = fake_author.password

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": author_email, "password": author_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    title: str = fake_article.title
    draft_data: dict = {"title": title}

    res = await async_client.post(
        "/api/v1/articles/drafts",
        json=draft_data,
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    json_res = res.json()

    assert res.status_code == 201
    assert title == json_res["data"]["title"]

@pytest.mark.asyncio
async def test_create_rating(create_article: Response, async_client: AsyncClient):
    user_email: str = fake_user.email
    user_password: str = fake_user.password

    article_json_res = create_article.json()
    article_id: str = article_json_res["data"]["id"]

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": user_email, "password": user_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    res = await async_client.post(
        f"/api/v1/articles/{article_id}/rate",
        data={"rating": 7.7},
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    assert res.status_code == 201


@pytest.mark.asyncio
async def test_upload_images(create_article: Response, async_client: AsyncClient):
    author_email: str = fake_author.email
    author_password: str = fake_author.password

    article_json_res = create_article.json()
    article_id: str = article_json_res["data"]["id"]

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": author_email, "password": author_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    file_path: Path = Path(__file__).parent.parent / "assets" / "20240811_012037.jpg"

    async with aiofiles.open(file_path) as img:
        res = await async_client.post(
            f"/api/v1/articles/{article_id}/images",
            files={"article_images": [("20240811_012037.jpg", img, "image/jpg")]},
            headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
        )

    json_res = res.json()
    img_res: ImageOutV1 = json_res["data"][0]

    assert res.status_code == 201
    assert img_res.img_name == "20240811_012037"

    # cleanup image
    img_path: Path = Path("app\\uploads\\football\\20240811_012037.jpg")

    assert img_path.exists()
    img_path.unlink()


@pytest.mark.asyncio
async def test_update_article(create_article: Response, async_client: AsyncClient):
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

    res = await async_client.patch(
        f"/api/v1/articles/{article_id}",
        json=article_update,
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    json_res = res.json()
    new_article_title: str = article_update.title

    assert res.status_code == 200
    assert new_article_title == json_res["data"]["title"]


@pytest.mark.asyncio
async def test_update_draft(
    create_author: Response, async_client: AsyncClient
):
    author_email: str = fake_author.email
    author_password: str = fake_author.password

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": author_email, "password": author_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    title: str = fake_article.title
    draft_data: dict = {"title": title}
    draft_update: dict = {"title": "new_fake_title"}


    draft_res = await async_client.post(
        "/api/v1/articles/drafts",
        json=draft_data,
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    draft_id: str = draft_res.json()["data"]["draft_id"]

    res = await async_client.patch(
        f"/api/v1/articles/drafts{draft_id}",
        json=draft_update,
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    json_res = res.json()

    assert res.status_code == 200
    assert title == json_res["data"]["title"]


@pytest.mark.asyncio
async def test_update_rating(create_article: Response, async_client: AsyncClient):
    user_email: str = fake_user.email
    user_password: str = fake_user.password

    article_json_res = create_article.json()
    article_id: str = article_json_res["data"]["id"]

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": user_email, "password": user_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    res = await async_client.patch(
        f"/api/v1/articles/{article_id}/rate",
        data={"rating": 7.7},
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    assert res.status_code == 200


@pytest.mark.asyncio
async def test_unauthorized_article_update(
    create_article: Response, async_client: AsyncClient
):
    article_json_res = create_article.json()
    article_id: str = article_json_res["data"]["id"]

    article_update: dict = {"title": "new_fake_title"}

    res = await async_client.patch(
        f"/api/v1/articles/{article_id}",
        json=article_update,
        headers={"curr_env": "testing"},
    )

    assert res.status_code == 401


@pytest.mark.asyncio
async def test_delete_article(create_article: Response, async_client: AsyncClient):
    admin_email: str = fake_admin.email
    admin_password: str = fake_admin.password

    article_json_res = create_article.json()
    article_id: str = article_json_res["data"]["id"]

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": admin_email, "password": admin_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    res = await async_client.delete(
        f"/api/v1/articles/{article_id}",
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    assert res.status_code == 204


@pytest.mark.asyncio
async def test_delete_draft(
    create_author: Response, async_client: AsyncClient
):
    author_email: str = fake_author.email
    author_password: str = fake_author.password

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": author_email, "password": author_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    title: str = fake_article.title
    draft_data: dict = {"title": title}


    draft_res = await async_client.post(
        "/api/v1/articles/drafts",
        json=draft_data,
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    draft_id: str = draft_res.json()["data"]["draft_id"]

    res = await async_client.delete(
        f"/api/v1/articles/drafts/{draft_id}",
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    assert res.status_code == 204


@pytest.mark.asyncio
async def test_unauthorized_article_delete(
    create_article: Response, async_client: AsyncClient
):
    author_email: str = fake_author.email
    author_password: str = fake_author.password

    article_json_res = create_article.json()
    article_id: str = article_json_res["data"]["id"]

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": author_email, "password": author_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    res = await async_client.delete(
        f"/api/v1/articles/{article_id}",
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    assert res.status_code == 403


@pytest.mark.asyncio
async def test_delete_rating(create_article: Response, async_client: AsyncClient):
    user_email: str = fake_user.email
    user_password: str = fake_user.password

    article_json_res = create_article.json()
    article_id: str = article_json_res["data"]["id"]

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": user_email, "password": user_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    res = await async_client.post(
        f"/api/v1/articles/{article_id}/rate",
        data={"rating": 7.7},
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    assert res.status_code == 201

    res = await async_client.delete(
        f"/api/v1/articles/{article_id}/remove-rating",
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    assert res.status_code == 204


@pytest.mark.asyncio
async def test_delete_images(create_article: Response, async_client: AsyncClient):
    author_email: str = fake_author.email
    author_password: str = fake_author.password

    article_json_res = create_article.json()
    article_id: str = article_json_res["data"]["id"]

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": author_email, "password": author_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    file_path: Path = Path(__file__).parent.parent / "assets" / "20240811_012037.jpg"

    async with aiofiles.open(file_path) as img:
        await async_client.post(
            f"/api/v1/articles/{article_id}/images",
            files={"article_images": [("20240811_012037.jpg", img, "image/jpg")]},
            headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
        )

    res = await async_client.request(
        "DELETE",
        f"/api/v1/artices/{article_id}/images",
        data={"article_images": ["20240811_012037"]},
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    assert res.status_code == 204

    # cleanup image
    img_path: Path = Path("app\\uploads\\football\\20240811_012037.jpg")

    assert img_path.exists()
    img_path.unlink()
