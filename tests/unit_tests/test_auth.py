import pytest
from beanie import PydanticObjectId
from unittest.mock import AsyncMock, patch
from pymongo.asynchronous.client_session import AsyncClientSession


from tests.unit_tests.conftest import base_path
from app.api.v1.schemas.auth import RefreshTokenV1
from app.core.exceptions import AuthenticationError
from app.api.v1.schemas.users import UserCreateV1, UserV1
from tests.unit_tests.fake_data import fake_user, fake_token
from app.api.v1.services.auth_service import auth_service_v1


@pytest.mark.asyncio
async def test_get_tokens():
    user_email: str = fake_user.email

    tokens = await auth_service_v1.get_tokens(user_email)
    assert tokens


@pytest.mark.asyncio
async def test_invalidate_token(get_session: AsyncClientSession):
    refresh_token: RefreshTokenV1 = fake_token

    path: str = f"{base_path}.auth_service.update_tokens"
    with patch(path, new_callable=AsyncMock) as token:
        await auth_service_v1.invalidate_token(refresh_token, get_session)

    token.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_user(
    get_user_by_email: AsyncMock, get_session: AsyncClientSession
):
    user_email: str = fake_user.email
    user_password: str = fake_user.password

    user_create: UserCreateV1 = UserCreateV1(email=user_email, password=user_password)
    get_user_by_email.return_value = None

    user_path: str = f"{base_path}.user_service.add_user_to_db"
    code_path: str = f"{base_path}.auth_service.add_code_to_db"
    email_path: str = f"{base_path}.auth_service.send_email_code"

    create_user_patch: AsyncMock = patch(user_path, new_callable=AsyncMock).start()
    code_db_patch: AsyncMock = patch(code_path, new_callable=AsyncMock).start()
    code_patch: AsyncMock = patch(email_path, new_callable=AsyncMock).start()

    user = await auth_service_v1.create_user(user_create, get_session)

    create_user_patch.stop()
    code_db_patch.stop()
    code_patch.stop()

    assert user

    get_user_by_email.assert_awaited_once()
    create_user_patch.assert_awaited_once()
    code_db_patch.assert_awaited_once()
    code_patch.assert_called_once()


@pytest.mark.asyncio
async def test_sign_in(get_user_by_email: AsyncMock, get_session: AsyncClientSession):
    get_user_by_email.return_value = fake_user

    user_email: str = fake_user.email
    user_password: str = fake_user.password

    path: str = f"{base_path}.auth_service.add_tokens_to_db"
    with patch(path, new_callable=AsyncMock) as auth_token:
        sign_in = await auth_service_v1.sign_in(user_email, user_password, get_session)

    assert sign_in

    get_user_by_email.assert_awaited_once()
    auth_token.assert_awaited_once()


@pytest.mark.asyncio
async def test_resend_email_code(
    get_user_by_id: AsyncMock, get_session: AsyncClientSession
):
    get_user_by_id.return_value = fake_user

    code_path: str = f"{base_path}.auth_service.add_code_to_db"
    email_path: str = f"{base_path}.auth_service.send_email_code"

    code_db_patch: AsyncMock = patch(code_path, new_callable=AsyncMock).start()
    code_patch: AsyncMock = patch(email_path, new_callable=AsyncMock).start()

    user_id: PydanticObjectId = PydanticObjectId()
    await auth_service_v1.resend_email_code(user_id, get_session)

    code_db_patch.stop()
    code_patch.stop()

    get_user_by_id.assert_awaited_once()
    code_db_patch.assert_awaited_once()
    code_patch.assert_called_once()


@pytest.mark.asyncio
async def test_create_new_token(
    get_user_by_email: AsyncMock,
    verify_token: AsyncMock,
    get_session: AsyncClientSession,
):
    refresh_token: str = "fake-refresh-token"
    get_user_by_email.return_value = fake_user

    auth_path: str = f"{base_path}.auth_service.add_tokens_to_db"
    token_update_path: str = f"{base_path}.auth_service.update_tokens"
    token_path: str = f"{base_path}.auth_service.invalidate_token"

    token_patch: AsyncMock = patch(token_path, new_callable=AsyncMock).start()
    token_update_patch: AsyncMock = patch(
        token_update_path, new_callable=AsyncMock
    ).start()
    auth_token_patch: AsyncMock = patch(auth_path, new_callable=AsyncMock).start()

    token = await auth_service_v1.create_new_token(refresh_token, get_session)

    token_update_patch.stop()
    auth_token_patch.stop()
    token_patch.stop()

    assert token

    get_user_by_email.assert_awaited_once()
    verify_token.assert_awaited_once()
    token_patch.assert_awaited_once()
    token_update_patch.assert_awaited_once()
    auth_token_patch.assert_awaited_once()


@pytest.mark.asyncio
async def test_verify_user(get_user_by_id: AsyncMock, get_session: AsyncClientSession):
    get_user_by_id.return_value = fake_user

    code_path: str = f"{base_path}.auth_service.get_verification_code"
    user_path: str = f"{base_path}.user_service.update_user"

    code_patch: AsyncMock = patch(code_path, new_callable=AsyncMock).start()
    user_patch: AsyncMock = patch(user_path, new_callable=AsyncMock).start()

    user_id: PydanticObjectId = PydanticObjectId()
    email_code: str = f"sign_in+randcode82653+{user_id}"

    code_patch.return_value = "rand82653"

    verified_user = await auth_service_v1.verify_user(email_code, get_session)

    code_patch.stop()
    user_patch.stop()

    assert verified_user

    get_user_by_id.assert_awaited_once()
    code_patch.assert_awaited_once()
    user_patch.assert_awaited_once()


@pytest.mark.asyncio
async def test_sign_out(
    verify_token: AsyncMock,
    get_session: AsyncClientSession,
):
    refresh_token: str = "fake-refresh-token"
    curr_user: UserV1 = fake_user

    token_path: str = f"{base_path}.auth_service.update_tokens"
    with patch(token_path, new_callable=AsyncMock) as token_db:
        await auth_service_v1.sign_out(curr_user, refresh_token, get_session)

    verify_token.assert_awaited_once()
    token_db.assert_awaited_once()


@pytest.mark.asyncio
async def test_sign_out_unauthenticated(
    get_session: AsyncClientSession,
):
    refresh_token: str = "fake-refresh-token"
    curr_user: UserV1 = fake_user

    with pytest.raises(AuthenticationError) as exc:
        await auth_service_v1.sign_out(curr_user, refresh_token, get_session)

    assert "User not authenticated" == str(exc.value)


@pytest.mark.asyncio
async def test_update_password(
    get_user_by_email: AsyncMock,
    verify_token: AsyncMock,
    get_session: AsyncClientSession,
):
    curr_user: UserV1 = fake_user
    curr_password: str = fake_user.password
    new_password: str = "new_fake_password"
    refresh_token: str = "fake-refresh-token"

    user: UserCreateV1 = UserCreateV1.model_validate(fake_user)
    get_user_by_email.return_value = user

    path: str = f"{base_path}.user_service.update_user"
    with patch(path, new_callable=AsyncMock) as user:
        user = await auth_service_v1.update_password(
            curr_user, refresh_token, curr_password, new_password, get_session
        )

    assert user

    get_user_by_email.assert_awaited_once()
    verify_token.assert_awaited_once()
    user.assert_awaited_once()


@pytest.mark.asyncio
async def test_reset_password(
    get_user_by_email: AsyncMock, get_session: AsyncClientSession
):
    user_email: str = fake_user.email
    user_password: str = fake_user.password

    get_user_by_email.return_value = fake_user

    # path: str = f"{base_path}.update_user"
    # with patch(path, new_callable=AsyncMock) as user:
    # await auth_service_v1.reset_password(user_email, user_password, get_session)

    #     user.assert_awaited_once()

    email_path: str = f"{base_path}.auth_service.send_email_code"
    token_path: str = f"{base_path}.auth_service.invalidate_token"

    email_patch: AsyncMock = patch(email_path, new_callable=AsyncMock).start()
    token_patch: AsyncMock = patch(token_path, new_callable=AsyncMock).start()

    user = await auth_service_v1.reset_password(user_email, user_password, get_session)

    email_patch.stop()
    token_patch.stop()

    assert user

    get_user_by_email.assert_awaited_once()
    email_patch.assert_called_once()
    token_patch.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_user(verify_token: AsyncMock, get_session: AsyncClientSession):
    user_password: str = fake_user.password
    refresh_token: str = "fake-refresh-token"
    curr_user: UserV1 = fake_user

    user_path: str = f"{base_path}.user_service.delete_user"
    token_path: str = f"{base_path}.auth_service.invalidate_token"
    token_update_path: str = f"{base_path}.auth_service.update_tokens"

    token_update_patch: AsyncMock = patch(
        token_update_path, new_callable=AsyncMock
    ).start()
    token_patch: AsyncMock = patch(token_path, new_callable=AsyncMock).start()
    user_patch: AsyncMock = patch(user_path, new_callable=AsyncMock).start()

    await auth_service_v1.delete_user(
        curr_user, refresh_token, user_password, get_session
    )

    user_patch.stop()
    token_patch.stop()
    token_update_patch.stop()

    user_patch.assert_awaited_once()
    verify_token.assert_awaited_once()
    token_patch.assert_awaited_once()
    token_update_patch.assert_awaited_once()
