import pytest_asyncio
from beanie import Document
from beanie import init_beanie
from pymongo import AsyncMongoClient
from httpx import AsyncClient, ASGITransport, Response
from pymongo.asynchronous.client_session import AsyncClientSession


from app.main import app
from app.database import client
from app.core.config import settings
from app.dependencies import get_session
from app.api.v1.schemas.tasks import TaskV1
from app.scripts.seeds.create_sports import SportCategory
from app.api.v1.schemas.auth import RefreshTokenV1, EmailCodeV1
from app.scripts.seeds.create_admin import create_admin_user as create_admin
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
from app.api.v1.schemas.users import (
    UserV1,
    AccountV1,
    AdminV1,
    AuthorV1,
    EditorV1,
    EmployeeV1,
    UserCreateV1,
    AdminCreateV1,
    AuthorCreateV1,
    EditorCreateV1,
)
from app.api.v1.schemas.articles import (
    ArticleV1,
    TeamSportV1,
    SubscriptionV1,
    ArticleCreateV1,
    IndividualSportV1,
)
from app.api.v1.schemas.sports import (
    GolfV1,
    SportV1,
    BoxingV1,
    TennisV1,
    FootballV1,
    BasketballV1,
)


@pytest_asyncio.fixture(scope="session")
async def initialize_db():
    db_name: str = settings.DB_NAME
    db = client[db_name]
    models: list[Document] = [
        UserV1,
        GolfV1,
        TaskV1,
        SportV1,
        AdminV1,
        AuthorV1,
        EditorV1,
        BoxingV1,
        TennisV1,
        AccountV1,
        ArticleV1,
        EmployeeV1,
        FootballV1,
        TeamSportV1,
        EmailCodeV1,
        BasketballV1,
        RefreshTokenV1,
        SubscriptionV1,
        IndividualSportV1,
    ]

    await init_beanie(db, document_models=models, allow_index_dropping=True)

    yield client

    for model in models:
        await model.get_pymongo_collection().drop()

    await client.close()


@pytest_asyncio.fixture
async def get_test_session(initialize_db: AsyncMongoClient):
    session: AsyncClientSession = initialize_db.start_session(causal_consistency=True)
    await session.start_transaction()

    yield session

    await session.abort_transaction()
    await session.end_session()


@pytest_asyncio.fixture
async def async_client(get_test_session: AsyncClientSession):
    async def get_db_session():
        yield get_test_session

    app.dependency_overrides[get_session] = get_db_session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost"
    ) as client:
        yield client


@pytest_asyncio.fixture
async def create_admin_user():
    admin_email: str = fake_admin.get("email")
    admin_password: str = fake_admin.get("password")
    admin_name: str = fake_admin.get("name")
    admin_nationality: str = fake_admin.get("nationality")

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


@pytest_asyncio.fixture
async def create_user(create_admin_user, create_sports, async_client: AsyncClient):
    user_email: str = fake_user.get("email")
    user_password: str = fake_user.get("password")

    user_create: UserCreateV1 = UserCreateV1(email=user_email, password=user_password)

    res = await async_client.post(
        "/api/v1/auth/sign-up", json=user_create, headers={"curr_env": "testing"}
    )

    return res


@pytest_asyncio.fixture
async def create_author(create_admin_user, create_sports, async_client: AsyncClient):
    admin_email: str = fake_admin.get("email")
    admin_password: str = fake_admin.get("password")

    author_name: str = fake_author.get("name")
    author_email: str = fake_author.get("email")
    author_password: str = fake_author.get("password")
    author_nationality: str = fake_author.get("nationality")

    sign_up_data: UserCreateV1 = UserCreateV1(
        email=author_email, password=author_password
    )

    await async_client.post(
        "/api/v1/auth/sign-up",
        json=sign_up_data,
        headers={"curr_env": "testing"},
    )

    author_create: AuthorCreateV1 = AuthorCreateV1(
        name=author_name, nationality=author_nationality
    )

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
async def create_editor(create_admin_user, create_sports, async_client: AsyncClient):
    admin_email: str = fake_admin.get("email")
    admin_password: str = fake_admin.get("password")

    editor_name: str = fake_editor.get("name")
    editor_email: str = fake_editor.get("email")
    editor_password: str = fake_editor.get("password")
    editor_nationality: str = fake_editor.get("nationality")

    sign_up_data: UserCreateV1 = UserCreateV1(
        email=editor_email, password=editor_password
    )

    await async_client.post(
        "/api/v1/auth/sign-up",
        json=sign_up_data,
        headers={"curr_env": "testing"},
    )

    editor_create: EditorCreateV1 = EditorCreateV1(
        name=editor_name, nationality=editor_nationality
    )

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
async def create_article(create_author, create_sports, async_client: AsyncClient):
    author_email: str = fake_author.get("email")
    author_password: str = fake_author.get("password")

    sign_in_res: Response = await async_client.post(
        "/api/v1/auth/sign-in",
        data={"username": author_email, "password": author_password},
        headers={"curr_env": "testing"},
    )

    access_token: str = sign_in_res.json()["access_token"]

    title: str = fake_article.get("title")
    content: str = fake_article.get("content")
    author: str = fake_article.get("author")
    sport: str = fake_article.get("sport")
    category: str = fake_article.get("category")
    athletes: list[str] = fake_article.get("athletes")

    article_create: ArticleCreateV1 = ArticleCreateV1(
        title=title,
        content=content,
        author=author,
        sport=sport,
        category=category,
        athletes=athletes,
    )

    res = await async_client.post(
        "/api/v1/articles",
        json=article_create,
        headers={"Authorization": f"Bearer {access_token}", "curr_env": "testing"},
    )

    return res
