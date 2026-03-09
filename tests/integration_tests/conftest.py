import pytest_asyncio
from typing import Any
from beanie import PydanticObjectId
from httpx import AsyncClient, Response
from unittest.mock import AsyncMock, patch
from collections.abc import AsyncGenerator


from app.api.v1.schemas.articles import ArticleCreateV1
from app.scripts.seeds.create_sports import SportCategory
from tests.integration_tests.database import async_client
from app.scripts.seeds.create_admin import create_admin_user as create_admin
from app.api.v1.schemas.users import (
    UserCreateV1,
    AdminCreateV1,
    AuthorCreateV1,
    EditorCreateV1,
)
from tests.fake_data import (
    fake_user,
    fake_admin,
    fake_author,
    fake_editor,
    fake_article,
    football_teams,
    basketball_teams,
    golf_competitions,
    tennis_competitions,
    boxing_competitions,
    football_competitions,
    basketball_competitions,
)


@pytest_asyncio.fixture
async def create_admin_user():
    admin_email: str = fake_admin.email
    admin_password: str = fake_admin.password
    admin_name: str = fake_admin.name
    admin_nationality: str = fake_admin.nationality

    sign_up_data: AdminCreateV1 = AdminCreateV1(
        email=admin_email,
        password=admin_password,
        name=admin_name,
        nationality=admin_nationality,
    )

    await create_admin(sign_up_data)


@pytest_asyncio.fixture
async def create_sports():
    golf_category = SportCategory(name="golf")
    tennis_category = SportCategory(name="tennis")
    boxing_category = SportCategory(name="boxing")
    football_category = SportCategory(name="football")
    basketball_category = SportCategory(name="basketball")

    await golf_category.add_golf(golf_competitions)
    await tennis_category.add_tennis(tennis_competitions)
    await boxing_category.add_boxing(boxing_competitions)
    await football_category.add_football(football_teams, football_competitions)
    await basketball_category.add_basketball(basketball_teams, basketball_competitions)


base_path: str = "app.api.v1.services"


@pytest_asyncio.fixture
async def send_email_code() -> AsyncGenerator[AsyncMock, Any, None]:
    path: str = f"{base_path}.auth_service.send_email_code"
    with patch(path, new_callable=AsyncMock) as email:
        yield email

    email.assert_awaited_once()


@pytest_asyncio.fixture
async def send_email_to_subscribers() -> AsyncGenerator[AsyncMock, Any, None]:
    path: str = f"{base_path}.article_service.send_email_to_subscribers"
    with patch(path, new_callable=AsyncMock) as email:
        yield email

    email.assert_awaited_once()


@pytest_asyncio.fixture
async def send_information_to_users() -> AsyncGenerator[AsyncMock, Any, None]:
    path: str = f"{base_path}.admin_service.send_information_to_users"
    with patch(path, new_callable=AsyncMock) as email:
        yield email

    email.assert_awaited_once()


@pytest_asyncio.fixture
async def send_newsletter_to_users() -> AsyncGenerator[AsyncMock, Any, None]:
    path: str = f"{base_path}.admin_service.send_newsletter_to_users"
    with patch(path, new_callable=AsyncMock) as email:
        yield email

    email.assert_awaited_once()


@pytest_asyncio.fixture
async def create_user(
    create_sports,
    create_admin_user,
    send_email_code: AsyncMock,
    async_client: AsyncClient,
) -> Response:
    user_email: str = fake_user.email
    user_password: str = fake_user.password

    user_create: UserCreateV1 = UserCreateV1(
        email=user_email,
        password=user_password,
    )

    res = await async_client.post(
        "/api/v1/auth/sign-up", json=user_create, headers={"curr_env": "testing"}
    )

    return res


@pytest_asyncio.fixture
async def create_author(
    create_sports,
    create_admin_user,
    send_email_code: AsyncMock,
    async_client: AsyncClient,
) -> Response:
    # author is initially created as a user
    admin_email: str = fake_admin.email
    admin_password: str = fake_admin.password

    author_name: str = fake_author.name
    author_email: str = fake_author.email
    author_password: str = fake_author.password
    author_nationality: str = fake_author.nationality

    sign_up_data: UserCreateV1 = UserCreateV1(
        email=author_email,
        password=author_password,
    )

    sign_up_res = await async_client.post(
        "/api/v1/auth/sign-up",
        json=sign_up_data,
        headers={"curr_env": "testing"},
    )

    sign_up_json = sign_up_res.json()
    author_id: PydanticObjectId = sign_up_json["data"]["id"]

    author_create: AuthorCreateV1 = AuthorCreateV1(
        name=author_name, nationality=author_nationality, user_id=author_id
    )

    # admin assigns author role to the created user
    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": admin_email, "password": admin_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    res = await async_client.post(
        "/api/v1/admin/authors",
        json=author_create,
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    return res


@pytest_asyncio.fixture
async def create_editor(
    create_sports,
    create_admin_user,
    send_email_code: AsyncMock,
    async_client: AsyncClient,
) -> Response:
    # editor is initially created as a user
    admin_email: str = fake_admin.email
    admin_password: str = fake_admin.password

    editor_name: str = fake_editor.name
    editor_email: str = fake_editor.email
    editor_password: str = fake_editor.password
    editor_nationality: str = fake_editor.nationality

    sign_up_data: UserCreateV1 = UserCreateV1(
        email=editor_email,
        password=editor_password,
    )

    sign_up_res = await async_client.post(
        "/api/v1/auth/sign-up",
        json=sign_up_data,
        headers={"curr_env": "testing"},
    )

    sign_up_json = sign_up_res.json()
    editor_id: PydanticObjectId = sign_up_json["data"]["id"]

    editor_create: EditorCreateV1 = EditorCreateV1(
        name=editor_name, nationality=editor_nationality, user_id=editor_id
    )

    # admin assigns editor role to the created user
    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": admin_email, "password": admin_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    res = await async_client.post(
        "/api/v1/admin/editors",
        json=editor_create,
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    return res


@pytest_asyncio.fixture
async def create_article(
    create_author, send_email_to_subscribers: AsyncMock, async_client: AsyncClient
) -> Response:
    author_email: str = fake_author.email
    author_password: str = fake_author.password

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": author_email, "password": author_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    title: str = fake_article.title
    content: str = fake_article.content
    author: str = fake_article.author.name
    sport: str = fake_article.sport.name
    category: str = fake_article.category
    teams: list[str] = [fake_article.teams[0].name]

    article_create: ArticleCreateV1 = ArticleCreateV1(
        title=title,
        content=content,
        author=author,
        sport=sport,
        category=category,
        teams=teams,
    )

    res = await async_client.post(
        "/api/v1/articles",
        json=article_create,
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    return res
