import pytest
from beanie import PydanticObjectId
from unittest.mock import AsyncMock, patch
from pymongo.asynchronous.client_session import AsyncClientSession


from tests.unit_tests.conftest import base_path
from app.api.v1.services.editor_service import editor_service_v1
from tests.fake_data import fake_editor, fake_article, fake_dashboard
from app.api.v1.schemas.users import WriterSettingsUpdateV1, EditorV1


@pytest.mark.asyncio
async def test_get_editor_articles(
    verify_token: AsyncMock, get_session: AsyncClientSession
):
    editor: EditorV1 = fake_editor
    refresh_token: str = "fake-refresh-token"

    path: str = f"{base_path}.editor_service.get_articles_from_db"
    with patch(path, new_callable=AsyncMock) as articles:
        articles.return_value = [fake_article]
        await editor_service_v1.get_articles(editor, refresh_token, get_session)

    verify_token.assert_awaited_once()
    articles.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_editor_dashboard(
    verify_token: AsyncMock, get_session: AsyncClientSession
):
    editor: EditorV1 = fake_editor
    refresh_token: str = "fake-refresh-token"

    path: str = f"{base_path}.editor_service.get_dashboard_from_db"
    with patch(path, new_callable=AsyncMock) as dashboard:
        dashboard.return_value = fake_dashboard
        await editor_service_v1.get_dashboard(editor, refresh_token, get_session)

    verify_token.assert_awaited_once()
    dashboard.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_editor_profile(
    verify_token: AsyncMock, get_session: AsyncClientSession
):
    editor: EditorV1 = fake_editor
    refresh_token: str = "fake-refresh-token"

    profile = await editor_service_v1.get_editor_profile(
        editor, refresh_token, get_session
    )

    assert profile


@pytest.mark.asyncio
async def test_get_editor_profile_settings(
    verify_token: AsyncMock, get_session: AsyncClientSession
):
    editor: EditorV1 = fake_editor
    refresh_token: str = "fake-refresh-token"

    profile_settings = await editor_service_v1.get_editor_profile_settings(
        editor, refresh_token, get_session
    )

    assert profile_settings
    verify_token.assert_awaited_once()


@pytest.mark.asyncio
async def test_mark_article_edited(
    verify_token: AsyncMock, get_session: AsyncClientSession
):
    editor: EditorV1 = fake_editor
    refresh_token: str = "fake-refresh-token"
    article_id: PydanticObjectId = PydanticObjectId()

    article_path: str = f"{base_path}.article_service.get_article_by_id"
    update_path: str = f"{base_path}.article_service.update_article_in_db"

    article_db = patch(article_path, new_callable=AsyncMock).start()
    article_update = patch(update_path, new_callable=AsyncMock).start()

    article_db.return_value = fake_article

    article = await editor_service_v1.mark_article_edited(
        editor, refresh_token, article_id, get_session
    )

    article_db.stop()
    article_update.stop()

    assert article

    verify_token.assert_awaited_once()
    article_db.assert_awaited_once()
    article_update.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_editor_profile_settings(
    verify_token: AsyncMock, get_session: AsyncClientSession
):
    editor: EditorV1 = fake_editor
    refresh_token: str = "fake-refresh-token"

    settings_update: WriterSettingsUpdateV1 = WriterSettingsUpdateV1(
        auto_delete_drafts=True
    )

    path: str = f"{base_path}.editor_service.update_editor_in_db"
    with patch(path, new_callable=AsyncMock) as settings:
        profile_settings = await editor_service_v1.update_user_profile_settings(
            editor, refresh_token, settings_update, get_session
        )

    assert profile_settings
    verify_token.assert_awaited_once()
    settings.assert_awaited_once()
