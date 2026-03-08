import pytest
from beanie import PydanticObjectId
from unittest.mock import AsyncMock, patch
from pymongo.asynchronous.client_session import AsyncClientSession


from tests.fake_data import fake_user
from tests.unit_tests.conftest import base_path
from app.api.v1.services.user_service import user_service_v1
from app.core.exceptions import AuthenticationError, UserNotFoundError
from app.api.v1.schemas.users import UserCreateV1, UserSettingsUpdateV1, UserV1


@pytest.mark.asyncio
async def test_create_user(get_session: AsyncClientSession):
    user_email: str = fake_user.email
    user_password: str = fake_user.password

    user_create: UserCreateV1 = UserCreateV1(email=user_email, password=user_password)

    path: str = f"{base_path}.auth_service.add_user_to_db"
    with patch(path, new_cllable=AsyncMock) as user:
        await user_service_v1.create_user(user_create, get_session)

    user.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_user_profile(
    verify_token: AsyncMock, get_session: AsyncClientSession
):
    curr_user: UserV1 = fake_user
    refresh_token: str = "fake-refresh-token"

    profile = await user_service_v1.get_user_profile(
        curr_user, refresh_token, get_session
    )

    assert profile
    verify_token.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_user_profile_settings(
    verify_token: AsyncMock, get_session: AsyncClientSession
):
    curr_user: UserV1 = fake_user
    refresh_token: str = "fake-refresh-token"

    profile_settings = await user_service_v1.get_user_profile_settings(
        curr_user, refresh_token, get_session
    )

    assert profile_settings
    verify_token.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_user_by_email(
    verify_token: AsyncMock,
    get_user_by_email: AsyncMock,
    get_session: AsyncClientSession,
):
    user_email: str = fake_user.email
    refresh_token: str = "fake-refresh-token"

    get_user_by_email.return_value = fake_user

    user = await user_service_v1.get_user_by_email(
        user_email, get_session, refresh_token
    )

    assert user
    get_user_by_email.assert_awaited_once()
    verify_token.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_user_by_id(
    verify_token: AsyncMock,
    get_user_by_id: AsyncMock,
    get_session: AsyncClientSession,
):
    user_id: PydanticObjectId = PydanticObjectId()
    refresh_token: str = "fake-refresh-token"

    get_user_by_id.return_value = fake_user

    user = await user_service_v1.get_user_by_id(user_id, get_session, refresh_token)

    assert user
    get_user_by_id.assert_awaited_once()
    verify_token.assert_awaited_once()


@pytest.mark.asyncio
async def test_user_not_found(
    verify_token: AsyncMock,
    get_session: AsyncClientSession,
):
    user_id: PydanticObjectId = PydanticObjectId()
    refresh_token: str = "fake-refresh-token"

    with pytest.raises(UserNotFoundError) as exc:
        await user_service_v1.get_user_by_id(user_id, get_session, refresh_token)

    assert "User not found" == str(exc.value)
    verify_token.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_user(
    verify_token: AsyncMock,
    get_session: AsyncClientSession,
):
    user: UserV1 = fake_user
    refresh_token: str = "fake-refresh-token"

    path: str = f"{base_path}.user_service.update_user_in_db"
    with patch(path, new_callable=AsyncMock) as user_update:
        await user_service_v1.update_user(user, get_session, refresh_token)

    verify_token.assert_awaited_once()
    user_update.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_unauthenticated_user(
    get_session: AsyncClientSession,
):
    user: UserV1 = fake_user
    refresh_token: str = "fake-refresh-token"

    with pytest.raises(AuthenticationError) as exc:
        await user_service_v1.update_user(user, get_session, refresh_token)

    assert "User not authenticated" == str(exc.value)


@pytest.mark.asyncio
async def test_update_user_profile_settings(
    verify_token: AsyncMock, get_session: AsyncClientSession
):
    user: UserV1 = fake_user
    refresh_token: str = "fake-refresh-token"
    settings_update: UserSettingsUpdateV1 = UserSettingsUpdateV1(
        receive_infomation=True
    )

    path: str = f"{base_path}.user_service.update_user_in_db"
    with patch(path, new_callable=AsyncMock) as settings:
        profile_settings = await user_service_v1.update_user_profile_settings(
            user, refresh_token, settings_update, get_session
        )

    assert profile_settings
    verify_token.assert_awaited_once()
    settings.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_user(
    verify_token: AsyncMock,
    get_session: AsyncClientSession,
):
    user: UserV1 = fake_user
    refresh_token: str = "fake-refresh-token"

    path: str = f"{base_path}.user_service.delete_user_from_db"
    with patch(path, new_callable=AsyncMock) as user_delete:
        await user_service_v1.delete_user(user, get_session, refresh_token)

    verify_token.assert_awaited_once()
    user_delete.assert_awaited_once()
