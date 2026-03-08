import pytest
from datetime import datetime
from beanie import PydanticObjectId
from unittest.mock import AsyncMock, patch
from pymongo.asynchronous.client_session import AsyncClientSession


from tests.unit_tests.conftest import base_path
from app.api.v1.schemas.articles import ArticleStatusV1
from app.api.v1.services.sport_service import admin_service_v1
from app.api.v1.schemas.users import AdminV1, EmployeeSettingsUpdateV1
from app.core.exceptions import AuthenticationError, AuthorNotFoundError
from tests.fake_data import (
    football,
    fake_user,
    fake_task,
    fake_admin,
    fake_author,
    fake_editor,
    fake_article,
    fake_dashboard_1,
    fake_author_create,
    fake_editor_create,
)


@pytest.mark.asyncio
async def test_get_admin_profile(
    verify_token: AsyncMock, get_session: AsyncClientSession
):
    admin: AdminV1 = fake_admin
    refresh_token: str = "fake-refresh-token"

    profile = await admin_service_v1.get_admin_profile(
        admin, refresh_token, get_session
    )

    assert profile
    verify_token.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_unauthenticated_admin_profile(get_session: AsyncClientSession):
    admin: AdminV1 = fake_admin
    refresh_token: str = "fake-refresh-token"

    with pytest.raises(AuthenticationError) as exc:
        await admin_service_v1.get_admin_profile(admin, refresh_token, get_session)

    assert "User not authenticated" == str(exc.value)


@pytest.mark.asyncio
async def test_get_admin_profile_settings(
    verify_token: AsyncMock, get_session: AsyncClientSession
):
    admin: AdminV1 = fake_admin
    refresh_token: str = "fake-refresh-token"

    profile_settings = await admin_service_v1.get_admin_profile_settings(
        admin, refresh_token, get_session
    )

    assert profile_settings
    verify_token.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_admin_dashboard(
    verify_token: AsyncMock, get_session: AsyncClientSession
):
    admin: AdminV1 = fake_admin
    refresh_token: str = "fake-refresh-token"

    path: str = f"{base_path}.admin_service.get_dashboard_from_db"
    with patch(path, new_callable=AsyncMock) as dashboard:
        dashboard.return_value = fake_dashboard_1
        admin_dashboard = await admin_service_v1.get_admin_dashboard(
            admin, refresh_token, get_session
        )

    assert admin_dashboard
    verify_token.assert_awaited_once()
    dashboard.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_all_users(verify_token: AsyncMock, get_session: AsyncClientSession):
    admin: AdminV1 = fake_admin
    refresh_token: str = "fake-refresh-token"

    path: str = f"{base_path}.admin_service.get_users_from_db"
    with patch(path, new_callable=AsyncMock) as users:
        users.return_value = [fake_user]
        users_db = await admin_service_v1.get_all_users(
            admin, refresh_token, get_session
        )

    assert users_db

    verify_token.assert_awaited_once()
    users.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_all_authors(
    verify_token: AsyncMock, get_session: AsyncClientSession
):
    admin: AdminV1 = fake_admin
    refresh_token: str = "fake-refresh-token"

    path: str = f"{base_path}.admin_service.get_authors_from_db"
    with patch(path, new_callable=AsyncMock) as authors:
        authors.return_value = [fake_author]
        authors_db = await admin_service_v1.get_all_authors(
            admin, refresh_token, get_session
        )

    assert authors_db

    verify_token.assert_awaited_once()
    authors.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_all_editors(
    verify_token: AsyncMock, get_session: AsyncClientSession
):
    admin: AdminV1 = fake_admin
    refresh_token: str = "fake-refresh-token"

    path: str = f"{base_path}.admin_service.get_editors_from_db"
    with patch(path, new_callable=AsyncMock) as editors:
        editors.return_value = [fake_editor]
        editors_db = await admin_service_v1.get_all_editors(
            admin, refresh_token, get_session
        )

    assert editors_db

    verify_token.assert_awaited_once()
    editors.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_all_articles(
    verify_token: AsyncMock, get_session: AsyncClientSession
):
    admin: AdminV1 = fake_admin
    refresh_token: str = "fake-refresh-token"

    path: str = f"{base_path}.admin_service.get_articles_from_db"
    with patch(path, new_callable=AsyncMock) as articles:
        articles.return_value = [fake_article]
        articles_db = await admin_service_v1.get_all_articles(
            admin, refresh_token, get_session
        )

    assert articles_db

    verify_token.assert_awaited_once()
    articles.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_article_readers(
    verify_token: AsyncMock, get_session: AsyncClientSession
):
    admin: AdminV1 = fake_admin
    refresh_token: str = "fake-refresh-token"

    path: str = f"{base_path}.admin_service.get_article_readers"

    start_date: datetime = datetime.now()
    end_date: datetime = datetime.now()

    with patch(path, new_callable=AsyncMock) as readers:
        readers.return_value = {"readers": 11}
        readers_db = await admin_service_v1.get_article_readers(
            admin, refresh_token, get_session, start_date, end_date
        )

    assert readers_db

    verify_token.assert_awaited_once()
    readers.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_all_sports(verify_token: AsyncMock, get_session: AsyncClientSession):
    admin: AdminV1 = fake_admin
    refresh_token: str = "fake-refresh-token"

    path: str = f"{base_path}.admin_service.get_all_sports"
    with patch(path, new_callable=AsyncMock) as sports:
        sports.return_value = [football]
        sports_db = await admin_service_v1.get_all_sports(
            admin, get_session, refresh_token
        )

    assert sports_db
    verify_token.assert_awaited_once()
    sports.assert_awaited_once()


@pytest.mark.asyncio
async def test_assign_article(verify_token: AsyncMock, get_session: AsyncClientSession):
    admin: AdminV1 = fake_admin
    refresh_token: str = "fake-refresh-token"

    editor_id: PydanticObjectId = PydanticObjectId()
    article_id: PydanticObjectId = PydanticObjectId()

    editor_path: str = f"{base_path}.user_service.get_user_by_id"
    article_path: str = f"{base_path}.article_service.get_article_by_id"
    task_path: str = f"{base_path}.admin_service.assign_article"

    editor_patch: AsyncMock = patch(editor_path, new_callable=AsyncMock).start()
    article_patch: AsyncMock = patch(article_path, new_callable=AsyncMock).start()
    task_patch: AsyncMock = patch(task_path, new_callable=AsyncMock).start()

    editor_patch.return_value = fake_editor
    task_patch.return_value = fake_task

    task = await admin_service_v1.assign_article(
        editor_id, article_id, admin, get_session, refresh_token
    )

    editor_patch.stop()
    article_patch.stop()
    task_patch.stop()

    assert task

    verify_token.assert_awaited_once()
    editor_patch.assert_awaited_once()
    article_patch.assert_awaited_once()
    task_patch.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_author(verify_token: AsyncMock, get_session: AsyncClientSession):
    admin: AdminV1 = fake_admin
    refresh_token: str = "fake-refresh-token"

    author_id: PydanticObjectId = PydanticObjectId()

    user_path: str = f"{base_path}.user_service.get_user_by_id"
    author_path: str = f"{base_path}.user_service.add_author_to_db"

    user_patch: AsyncMock = patch(user_path, new_callable=AsyncMock).start()
    author_patch: AsyncMock = patch(author_path, new_callable=AsyncMock).start()

    user_patch.return_value = fake_author
    author_patch.return_value = fake_author

    author = await admin_service_v1.create_author(
        author_id, fake_author_create, admin, get_session, refresh_token
    )

    user_patch.stop()
    author_patch.stop()

    assert author

    verify_token.assert_awaited_once()
    user_patch.assert_awaited_once()
    author_patch.assert_awaited_once()


@pytest.mark.asyncio
async def test_author_not_found(verify_token: AsyncMock, get_session: AsyncClientSession):
    admin: AdminV1 = fake_admin
    refresh_token: str = "fake-refresh-token"

    author_id: PydanticObjectId = PydanticObjectId()

    user_path: str = f"{base_path}.user_service.get_user_by_id"
    user_patch: AsyncMock = patch(user_path, new_callable=AsyncMock).start()

    user_patch.return_value = None

    with pytest.raises(AuthorNotFoundError) as exc:
        await admin_service_v1.create_author(
            author_id, fake_author_create, admin, get_session, refresh_token
        )

    assert "Author not found" == str(exc.value)

    user_patch.stop()

    verify_token.assert_awaited_once()
    user_patch.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_editor(verify_token: AsyncMock, get_session: AsyncClientSession):
    admin: AdminV1 = fake_admin
    refresh_token: str = "fake-refresh-token"

    editor_id: PydanticObjectId = PydanticObjectId()

    user_path: str = f"{base_path}.user_service.get_user_by_id"
    authro_path: str = f"{base_path}.user_service.add_editor_to_db"

    user_patch: AsyncMock = patch(user_path, new_callable=AsyncMock).start()
    editor_patch: AsyncMock = patch(authro_path, new_callable=AsyncMock).start()

    user_patch.return_value = fake_editor
    editor_patch.return_value = fake_editor

    editor = await admin_service_v1.create_editor(
        editor_id, fake_editor_create, admin, get_session, refresh_token
    )

    user_patch.stop()
    editor_patch.stop()

    assert editor

    verify_token.assert_awaited_once()
    user_patch.assert_awaited_once()
    editor_patch.assert_awaited_once()


@pytest.mark.asyncio
async def test_send_information(
    verify_token: AsyncMock, get_session: AsyncClientSession
):
    admin: AdminV1 = fake_admin
    refresh_token: str = "fake-refresh-token"

    path: str = f"{base_path}.admin_service.send_information_to_users"
    with patch(path, new_callable=AsyncMock) as info:
        await admin_service_v1.send_information(admin, get_session, refresh_token)

    verify_token.assert_awaited_once()
    info.assert_awaited_once()


@pytest.mark.asyncio
async def test_send_newsletter(
    verify_token: AsyncMock, get_session: AsyncClientSession
):
    admin: AdminV1 = fake_admin
    refresh_token: str = "fake-refresh-token"

    path: str = f"{base_path}.admin_service.send_newsletter_to_users"
    with patch(path, new_callable=AsyncMock) as news:
        await admin_service_v1.send_newsletter(admin, get_session, refresh_token)

    verify_token.assert_awaited_once()
    news.assert_awaited_once()


@pytest.mark.asyncio
async def test_publish_article(
    verify_token: AsyncMock, get_session: AsyncClientSession
):
    admin: AdminV1 = fake_admin
    refresh_token: str = "fake-refresh-token"

    fake_article.status = ArticleStatusV1.EDITED
    article_id: PydanticObjectId = PydanticObjectId()

    article_path: str = f"{base_path}.article_service.get_article_by_id"
    publish_path: str = f"{base_path}.article_service.update_article_in_db"

    article_patch: AsyncMock = patch(article_path, new_callable=AsyncMock).start()
    publish_patch: AsyncMock = patch(publish_path, new_callable=AsyncMock).start()

    article_patch.return_value = fake_article

    article = await admin_service_v1.publish_article(
        article_id, admin, get_session, refresh_token
    )

    article_patch.stop()
    publish_patch.stop()

    assert article

    verify_token.assert_awaited_once()
    article_patch.assert_awaited_once()
    publish_patch.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_admin_profile_settings(
    verify_token: AsyncMock, get_session: AsyncClientSession
):
    admin: AdminV1 = fake_admin
    refresh_token: str = "fake-refresh-token"

    settings_update: EmployeeSettingsUpdateV1 = EmployeeSettingsUpdateV1(theme="black")

    path: str = f"{base_path}.admin_service.update_admin_in_db"
    with patch(path, new_callable=AsyncMock) as settings:
        profile_settings = await admin_service_v1.update_admin_profile_settings(
            admin, refresh_token, settings_update, get_session
        )

    assert profile_settings
    verify_token.assert_awaited_once()
    settings.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_author(
    verify_token: AsyncMock, get_session: AsyncClientSession
):
    admin: AdminV1 = fake_admin
    refresh_token: str = "fake-refresh-token"

    author_id: PydanticObjectId = PydanticObjectId()

    user_path: str = f"{base_path}.user_service.get_user_by_id"
    author_path: str = f"{base_path}.admin_service.delete_author_from_db"

    user_patch: AsyncMock = patch(user_path, new_callable=AsyncMock).start()
    author_patch: AsyncMock = patch(author_path, new_callable=AsyncMock).start()

    author_patch.return_value = fake_author

    await admin_service_v1.delete_author(
        author_id, admin, refresh_token, get_session
    )

    user_patch.stop()
    author_patch.stop()

    verify_token.assert_awaited_once()
    user_patch.assert_awaited_once()
    author_patch.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_editor(
    verify_token: AsyncMock, get_session: AsyncClientSession
):
    admin: AdminV1 = fake_admin
    refresh_token: str = "fake-refresh-token"

    editor_id: PydanticObjectId = PydanticObjectId()

    user_path: str = f"{base_path}.user_service.get_user_by_id"
    editor_path: str = f"{base_path}.admin_service.delete_editor_from_db"

    user_patch: AsyncMock = patch(user_path, new_callable=AsyncMock).start()
    editor_patch: AsyncMock = patch(editor_path, new_callable=AsyncMock).start()

    editor_patch.return_value = fake_editor

    await admin_service_v1.delete_editor(
        editor_id, admin, refresh_token, get_session
    )

    user_patch.stop()
    editor_patch.stop()

    verify_token.assert_awaited_once()
    user_patch.assert_awaited_once()
    editor_patch.assert_awaited_once()
