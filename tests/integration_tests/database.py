import pytest
import pytest_asyncio
from typing import Any
from beanie import Document
from beanie import init_beanie
from pymongo import AsyncMongoClient
from collections.abc import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from pymongo.asynchronous.client_session import AsyncClientSession


from app.main import app
from app.core.config import settings
from app.dependencies import get_session
from app.database.models import db_models


@pytest_asyncio.fixture(scope="session")
async def initialize_db():
    client = AsyncMongoClient(
        settings.MONGO_DB_URI,
        tz_aware=True,
        maxConnecting=5,
        appname=settings.API_TITLE,
        tls=settings.ENVIRONMENT == "production",
    )

    db_name: str = settings.TEST_DB_NAME
    db = client[db_name]

    models: list[Document] = db_models

    await init_beanie(db, document_models=models, allow_index_dropping=True)

    yield client

    for model in models:
        await model.get_pymongo_collection().drop()

    await client.close()


@pytest_asyncio.fixture
async def get_test_session(
    initialize_db: AsyncMongoClient,
) -> AsyncGenerator[AsyncClientSession, Any, None]:
    session: AsyncClientSession = initialize_db.start_session(causal_consistency=True)
    await session.start_transaction()

    yield session

    await session.abort_transaction()
    await session.end_session()


@pytest_asyncio.fixture
async def async_client(
    get_test_session: AsyncClientSession,
) -> AsyncGenerator[AsyncClientSession, Any, None]:
    async def get_db_session():
        yield get_test_session

    app.dependency_overrides[get_session] = get_db_session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost"
    ) as client:
        yield client


# initiate beanie with pydantic models
@pytest.mark.asyncio
async def test_initiate_beanie(async_client):
    pass


pytest.main(["tests\\integration_tests\\database.py::test_initiate_beanie"])
