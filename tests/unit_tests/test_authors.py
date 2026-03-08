import pytest
from unittest.mock import AsyncMock, patch
from pymongo.asynchronous.client_session import AsyncClientSession


from tests.unit_tests.conftest import base_path
from app.api.v1.services.author_service import author_service_v1
from tests.fake_data import fake_author, fake_article, fake_dashboard
from app.api.v1.schemas.users import WriterSettingsUpdateV1, AuthorV1
from app.core.exceptions import AuthenticationError, ArticlesNotFoundError


@pytest.mark.asyncio
async def test_get_author_articles(
    verify_token: AsyncMock, get_session: AsyncClientSession
):
    author: AuthorV1 = fake_author
    refresh_token: str = "fake-refresh-token"

    path: str = f"{base_path}.author_service.get_articles_from_db"
    with patch(path, new_callable=AsyncMock) as articles:
        articles.return_value = [fake_article]
        author_articles = await author_service_v1.get_author_articles(
            author, refresh_token, get_session
        )

    assert author_articles
    verify_token.assert_awaited_once()
    articles.assert_awaited_once()


@pytest.mark.asyncio
async def test_author_articles_not_found(
    verify_token: AsyncMock, get_session: AsyncClientSession
):
    author: AuthorV1 = fake_author
    refresh_token: str = "fake-refresh-token"

    path: str = f"{base_path}.author_service.get_articles_from_db"

    author_articles = patch(path, new_callable=AsyncMock).start()
    author_articles.return_value = []

    with pytest.raises(ArticlesNotFoundError) as exc:
        await author_service_v1.get_author_articles(author, refresh_token, get_session)

    author_articles.stop()

    assert "Articles not found" == str(exc.value)
    verify_token.assert_awaited_once()
    author_articles.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_author_dashboard(
    verify_token: AsyncMock, get_session: AsyncClientSession
):
    author: AuthorV1 = fake_author
    refresh_token: str = "fake-refresh-token"

    path: str = f"{base_path}.author_service.get_dashboard_from_db"
    with patch(path, new_callable=AsyncMock) as dashboard:
        dashboard.return_value = fake_dashboard
        author_dashboard = await author_service_v1.get_author_dashboard(
            author, refresh_token, get_session
        )

    assert author_dashboard
    verify_token.assert_awaited_once()
    dashboard.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_author_profile(
    verify_token: AsyncMock, get_session: AsyncClientSession
):
    author: AuthorV1 = fake_author
    refresh_token: str = "fake-refresh-token"

    profile = await author_service_v1.get_author_profile(
        author, refresh_token, get_session
    )

    assert profile
    verify_token.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_unauthenticated_author_profile(
    get_session: AsyncClientSession
):
    author: AuthorV1 = fake_author
    refresh_token: str = "fake-refresh-token"

    with pytest.raises(AuthenticationError) as exc:
        await author_service_v1.get_author_profile(
            author, refresh_token, get_session
        )

    assert "User not authenticated" == str(exc.value)


@pytest.mark.asyncio
async def test_get_author_profile_settings(
    verify_token: AsyncMock, get_session: AsyncClientSession
):
    author: AuthorV1 = fake_author
    refresh_token: str = "fake-refresh-token"

    profile_settings = await author_service_v1.get_author_profile_settings(
        author, refresh_token, get_session
    )

    assert profile_settings
    verify_token.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_author_profile_settings(
    verify_token: AsyncMock, get_session: AsyncClientSession
):
    author: AuthorV1 = fake_author
    refresh_token: str = "fake-refresh-token"

    settings_update: WriterSettingsUpdateV1 = WriterSettingsUpdateV1(
        auto_delete_drafts=True
    )

    path: str = f"{base_path}.author_service.update_author_in_db"
    with patch(path, new_callable=AsyncMock) as settings:
        profile_settings = await author_service_v1.update_author_profile_settings(
            author, refresh_token, settings_update, get_session
        )

    assert profile_settings
    verify_token.assert_awaited_once()
    settings.assert_awaited_once()
