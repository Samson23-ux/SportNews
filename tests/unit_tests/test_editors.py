import pytest
from beanie import PydanticObjectId
from unittest.mock import AsyncMock, patch
from pymongo.asynchronous.client_session import AsyncClientSession


from tests.unit_tests.conftest import base_path
from app.api.v1.services.editor_service import editor_service_v1
from app.api.v1.schemas.users import WriterSettingsUpdateV1, EditorV1
from app.core.exceptions import AuthenticationError, ArticlesNotFoundError
from tests.unit_tests.fake_data import fake_editor, fake_article, fake_dashboard


@pytest.mark.asyncio
async def test_get_editor_articles(
    verify_token: AsyncMock, get_session: AsyncClientSession
):
    editor: EditorV1 = fake_editor
    refresh_token: str = "fake-refresh-token"

    path: str = f"{base_path}.editor_service.get_articles_from_db"
    with patch(path, new_callable=AsyncMock) as articles:
        articles.return_value = [fake_article]
        await editor_service_v1.get_editor_articles(editor, refresh_token, get_session)

    verify_token.assert_awaited_once()
    articles.assert_awaited_once()


@pytest.mark.asyncio
async def test_editor_articles_not_found(
    verify_token: AsyncMock, get_session: AsyncClientSession
):
    editor: EditorV1 = fake_editor
    refresh_token: str = "fake-refresh-token"

    path: str = f"{base_path}.editor_service.get_articles_from_db"

    editor_articles = patch(path, new_callable=AsyncMock).start()
    editor_articles.return_value = []

    with pytest.raises(ArticlesNotFoundError) as exc:
        await editor_service_v1.get_editor_articles(editor, refresh_token, get_session)

    editor_articles.stop()

    assert "Articles not found" == str(exc.value)
    verify_token.assert_awaited_once()
    editor_articles.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_editor_dashboard(
    verify_token: AsyncMock, get_session: AsyncClientSession
):
    editor: EditorV1 = fake_editor
    refresh_token: str = "fake-refresh-token"

    path: str = f"{base_path}.editor_service.get_dashboard_from_db"
    with patch(path, new_callable=AsyncMock) as dashboard:
        dashboard.return_value = fake_dashboard
        await editor_service_v1.get_editor_dashboard(editor, refresh_token, get_session)

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
async def test_get_unauthenticated_editor_profile(get_session: AsyncClientSession):
    editor: EditorV1 = fake_editor
    refresh_token: str = "fake-refresh-token"

    with pytest.raises(AuthenticationError) as exc:
        await editor_service_v1.get_editor_profile(editor, refresh_token, get_session)

    assert "User not authenticated" == str(exc.value)


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
    verify_token: AsyncMock, get_article_by_id: AsyncMock, get_session: AsyncClientSession
):
    editor: EditorV1 = fake_editor
    refresh_token: str = "fake-refresh-token"

    get_article_by_id.return_value = fake_article
    article_id: PydanticObjectId = PydanticObjectId()

    update_path: str = f"{base_path}.article_service.update_article_in_db"
    with patch(update_path, new_callable=AsyncMock) as article:
        article = await editor_service_v1.mark_article_edited(
            editor, refresh_token, article_id, get_session
        )

    assert article

    verify_token.assert_awaited_once()
    get_article_by_id.assert_awaited_once()
    article.assert_awaited_once()


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
        profile_settings = await editor_service_v1.update_editor_profile_settings(
            editor, refresh_token, settings_update, get_session
        )

    assert profile_settings
    verify_token.assert_awaited_once()
    settings.assert_awaited_once()
