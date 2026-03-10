import pytest_asyncio
from typing import Any
from collections.abc import AsyncGenerator
from unittest.mock import patch, AsyncMock


# from app.core.config import settings
# from tests.fake_data import fake_user
# from app.api.v1.schemas.users import UserCreateV1
# from app.api.v1.services.auth_service import auth_service_v1


base_path: str = "app.api.v1.services"


@pytest_asyncio.fixture
async def get_session() -> AsyncGenerator[AsyncMock, Any, None]:
    # mock mongo session
    path: str = "app.dependencies.get_session"
    with patch(path, new_callable=AsyncMock) as session:
        yield session


# mock repo functions to prevent actual interactions with the db
@pytest_asyncio.fixture
async def get_user_by_email() -> AsyncGenerator[AsyncMock, Any, None]:
    path: str = f"{base_path}.user_service.get_user_by_email"
    with patch(path, new_callable=AsyncMock) as user:
        yield user


@pytest_asyncio.fixture
async def get_user_by_id() -> AsyncGenerator[AsyncMock, Any, None]:
    path: str = f"{base_path}.user_service.get_user_by_id"
    with patch(path, new_callable=AsyncMock) as user:
        yield user


@pytest_asyncio.fixture
async def get_article_by_id() -> AsyncGenerator[AsyncMock, Any, None]:
    path: str = f"{base_path}.article_service.get_article_by_id"
    with patch(path, new_callable=AsyncMock) as article:
        yield article

    
@pytest_asyncio.fixture
async def verify_token() -> AsyncGenerator[AsyncMock, Any, None]:
    token_path: str = f"{base_path}.verify_refresh_token"
    with patch(token_path, new_callable=AsyncMock) as token:
        token.return_value = "fake-refresh-token"


# @pytest_asyncio.fixture
# async def create_user(
#     get_user_by_email: AsyncMock, get_session: AsyncClientSession
# ) -> AsyncGenerator[AsyncMock, Any, None]:
#     get_user_by_email.return_value = None

#     path: str = f"{base_path}.add_user_to_db"
#     with patch(path, new_callable=AsyncMock) as create_user:
#         user_create: UserCreateV1 = UserCreateV1.model_validate(fake_user)
#         await auth_service_v1.create_user(user_create, get_session)

#     email_path: str = "app.tasks.celery_task.send_email_code"
#     with patch(email_path, new_callable=AsyncMock) as _:
#         pass

#         yield create_user


# @pytest_asyncio.fixture
# async def sign_in(
#     get_user_by_email: AsyncMock, get_session: AsyncClientSession
# ) -> AsyncGenerator[AsyncMock, Any, None]:
#     user: UserCreateV1 = UserCreateV1.model_validate(fake_user)
    # get_user_by_email.return_value = user

    # user_email: str = fake_user.get("email")
    # user_password: str = fake_user.get("password")

    # path: str = f"{base_path}.add_tokens_to_db"
    # with patch(path, new_callable=AsyncMock) as auth_token:
    #     await auth_service_v1.sign_in(user_email, user_password, get_session)

    #     yield auth_token
