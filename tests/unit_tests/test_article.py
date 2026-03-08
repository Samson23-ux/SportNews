import pytest
import aiofiles
from pathlib import Path
from decimal import Decimal
from fastapi import UploadFile
from beanie import PydanticObjectId
from unittest.mock import AsyncMock, patch
from pymongo.asynchronous.client_session import AsyncClientSession


from tests.unit_tests.conftest import base_path
from app.api.v1.services.article_service import article_service_v1
from app.api.v1.schemas.users import UserV1, AuthorV1, EditorV1, AdminV1
from app.core.exceptions import AuthenticationError, ArticlesNotFoundError
from app.api.v1.schemas.articles import ArticleUpdateV1, ArticleDraftCreateV1
from tests.fake_data import (
    football,
    fake_user,
    fake_draft,
    fake_admin,
    fake_author,
    fake_user_1,
    fake_editor,
    fake_article,
    fake_draft_create,
    fake_article_create,
    fake_article_with_rating,
)


@pytest.mark.asyncio
async def test_get_articles(verify_token: AsyncMock, get_session: AsyncClientSession):
    curr_user: UserV1 = fake_user
    refresh_token: str = "fake-refresh-token"

    path: str = f"{base_path}.article_service.get_articles"
    with patch(path, new_callable=AsyncMock) as articles:
        articles.return_value = [fake_article]
        articles_db = await article_service_v1.get_articles(
            curr_user, refresh_token, get_session
        )

    assert articles_db

    verify_token.assert_awaited_once()
    articles.assert_awaited_once()


@pytest.mark.asyncio
async def test_articles_not_found(
    verify_token: AsyncMock, get_session: AsyncClientSession
):
    curr_user: UserV1 = fake_user
    refresh_token: str = "fake-refresh-token"

    path: str = f"{base_path}.article_service.get_articles"

    articles_patch = patch(path, new_callable=AsyncMock).start()
    articles_patch.return_value = []

    with pytest.raises(ArticlesNotFoundError) as exc:
        articles_db = await article_service_v1.get_articles(
            curr_user, refresh_token, get_session
        )

    articles_patch.stop()
    assert not articles_db
    assert "Articles not found" == str(exc.value)

    verify_token.assert_awaited_once()
    articles_patch.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_article(verify_token: AsyncMock, get_session: AsyncClientSession):
    curr_user: UserV1 = fake_user
    refresh_token: str = "fake-refresh-token"

    article_id: PydanticObjectId = PydanticObjectId()

    path: str = f"{base_path}.article_service.get_article_by_id"
    with patch(path, new_callable=AsyncMock) as article:
        article.return_value = fake_article
        article_db = await article_service_v1.get_article(
            article_id, curr_user, get_session, refresh_token
        )

    assert article_db

    verify_token.assert_awaited_once()
    article.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_article_unauthenticated(get_session: AsyncClientSession):
    curr_user: UserV1 = fake_user
    refresh_token: str = "fake-refresh-token"

    article_id: PydanticObjectId = PydanticObjectId()

    with pytest.raises(AuthenticationError) as exc:
        await article_service_v1.get_article(
            article_id, curr_user, refresh_token, get_session
        )

    assert "User not authenticated" == str(exc.value)


@pytest.mark.asyncio
async def test_get_drafts(verify_token: AsyncMock, get_session: AsyncClientSession):
    curr_user: AuthorV1 = fake_author
    refresh_token: str = "fake-refresh-token"

    path: str = f"{base_path}.article_service.get_drafts"
    with patch(path, new_callable=AsyncMock) as drafts:
        drafts.return_value = [fake_draft]
        drafts_db = await article_service_v1.get_drafts(
            curr_user, refresh_token, get_session
        )

    assert drafts_db

    verify_token.assert_awaited_once()
    drafts.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_draft(verify_token: AsyncMock, get_session: AsyncClientSession):
    curr_user: AuthorV1 = fake_author
    refresh_token: str = "fake-refresh-token"

    draft_id: PydanticObjectId = PydanticObjectId()

    path: str = f"{base_path}.article_service.get_draft_by_id"
    with patch(path, new_callable=AsyncMock) as draft:
        draft.return_value = fake_draft
        draft_db = await article_service_v1.get_draft(
            draft_id, curr_user, refresh_token, get_session
        )

    assert draft_db

    verify_token.assert_awaited_once()
    draft.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_article_images(
    verify_token: AsyncMock, get_session: AsyncClientSession
):
    curr_user: UserV1 = fake_user
    refresh_token: str = "fake-refresh-token"
    fake_image_url: str = "image_url3535"

    article_id: PydanticObjectId = PydanticObjectId()

    img_path: str = f"{base_path}.article_service.get_article_images"
    zip_path: str = f"{base_path}.article_service.zip_files"

    img_patch: AsyncMock = patch(img_path, new_callable=AsyncMock).start()
    zip_patch: AsyncMock = patch(zip_path, new_callable=AsyncMock).start()

    img_patch.return_value = [fake_image_url]

    article_images = await article_service_v1.get_article_images(
        curr_user, refresh_token, article_id, get_session
    )

    img_patch.close()
    zip_patch.close()

    assert article_images

    verify_token.assert_awaited_once()
    img_patch.assert_awaited_once()
    zip_patch.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_article(verify_token: AsyncMock, get_session: AsyncClientSession):
    curr_user: AuthorV1 = fake_author
    refresh_token: str = "fake-refresh-token"

    article_path: str = f"{base_path}.article_service.get_article_by_id"
    email_path: str = f"{base_path}.article_service.send_email_to_subscribers"
    article_create_path: str = f"{base_path}.article_service.add_article_to_db"
    sport_path: str = f"{base_path}.sport_service.get_sport_by_name"

    article_patch = patch(article_path, new_callable=AsyncMock).start()
    article_create_patch = patch(article_create_path, new_callable=AsyncMock).start()
    email_patch: AsyncMock = patch(email_path, new_callable=AsyncMock).start()
    sport_patch: AsyncMock = patch(sport_path, new_callable=AsyncMock).start()

    article_patch.return_value = fake_article
    sport_patch.return_value = football

    article = await article_service_v1.create_article(
        curr_user, refresh_token, fake_article_create, get_session
    )

    article_patch.stop()
    article_create_patch.stop()
    email_patch.stop()
    sport_patch.stop()

    assert article

    verify_token.assert_awaited_once()
    article_create_patch.assert_awaited_once()
    email_patch.assert_called_once()
    sport_patch.assert_awaited_once()
    article_patch.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_draft(verify_token: AsyncMock, get_session: AsyncClientSession):
    curr_user: AuthorV1 = fake_author
    refresh_token: str = "fake-refresh-token"

    draft_path: str = f"{base_path}.article_service.get_draft_by_id"
    draft_create_path: str = f"{base_path}.article_service.add_draft_to_db"

    draft_patch: AsyncMock = patch(draft_path, new_callable=AsyncMock).start()
    draft_create_patch: AsyncMock = patch(
        draft_create_path, new_callable=AsyncMock
    ).start()

    draft_patch.return_value = fake_draft

    draft = await article_service_v1.create_draft(
        curr_user, refresh_token, fake_draft_create, get_session
    )

    draft_patch.stop()
    draft_create_patch.stop()

    assert draft

    verify_token.assert_awaited_once()
    draft_create_patch.assert_awaited_once()
    draft_patch.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_rating(verify_token: AsyncMock, get_session: AsyncClientSession):
    curr_user: UserV1 = fake_user
    refresh_token: str = "fake-refresh-token"

    article_rating: Decimal = Decimal(7.7)
    article_id: PydanticObjectId = PydanticObjectId()

    article_path: str = f"{base_path}.article_service.get_article_by_id"
    rating_path: str = f"{base_path}.article_service.create_rating"

    article_patch: AsyncMock = patch(article_path, new_callable=AsyncMock).start()
    rating_patch: AsyncMock = patch(rating_path, new_callable=AsyncMock).start()

    article_patch.return_value = fake_article

    article = await article_service_v1.create_article_rating(
        curr_user, refresh_token, article_id, article_rating, get_session
    )

    article_patch.stop()
    rating_patch.stop()

    assert article

    verify_token.assert_awaited_once()
    article_patch.assert_awaited_once()
    rating_patch.assert_awaited_once()


@pytest.mark.asyncio
async def test_upload_article_images(
    verify_token: AsyncMock, get_session: AsyncClientSession
):
    curr_user: AuthorV1 = fake_author
    refresh_token: str = "fake-refresh-token"

    article_id: PydanticObjectId = PydanticObjectId()
    img_path: Path = Path(__file__).parent.parent / "assets" / "20240811_012037.jpg"

    file_path: str = f"{base_path}.article_service.write_file"
    article_img_path: str = f"{base_path}.article_service.add_article_image"
    article_path: str = f"{base_path}.article_service.get_article_by_id"

    file_patch: AsyncMock = patch(file_path, new_callable=AsyncMock).start()
    img_patch: AsyncMock = patch(article_img_path, new_callable=AsyncMock).start()
    article_patch = patch(article_path, new_callable=AsyncMock).start()

    async with aiofiles.open(img_path, "rb+") as file:
        upload_file: UploadFile = [UploadFile(file)]

    article_images = await article_service_v1.upload_article_images(
        curr_user, refresh_token, article_id, upload_file, get_session
    )

    file_patch.stop()
    img_patch.stop()
    article_patch.stop()

    assert article_images

    verify_token.assert_awaited_once()
    file_patch.assert_awaited_once()
    img_patch.assert_awaited_once()
    article_patch.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_article(verify_token: AsyncMock, get_session: AsyncClientSession):
    curr_user: EditorV1 = fake_editor
    refresh_token: str = "fake-refresh-token"

    new_title: str = "new_fake_title"
    article_id: PydanticObjectId = PydanticObjectId()

    article_update: ArticleUpdateV1 = ArticleUpdateV1(title=new_title)

    article_path: str = f"{base_path}.article_service.get_article_by_id"
    update_path: str = f"{base_path}.article_service.update_article_in_db"

    article_patch: AsyncMock = patch(article_path, new_callable=AsyncMock).start()
    article_update_patch: AsyncMock = patch(update_path, new_callable=AsyncMock).start()

    article_patch.return_value = fake_article

    article = await article_service_v1.update_article(
        curr_user, article_update, article_id, get_session, refresh_token,
    )

    article_patch.stop()
    article_update_patch.stop()

    assert article

    verify_token.assert_awaited_once()
    article_patch.assert_awaited_once()
    article_update_patch.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_draft(verify_token: AsyncMock, get_session: AsyncClientSession):
    curr_user: AuthorV1 = fake_author
    refresh_token: str = "fake-refresh-token"

    new_title: str = "new_fake_title"
    draft_id: PydanticObjectId = PydanticObjectId()

    draft_update: ArticleDraftCreateV1 = ArticleDraftCreateV1(title=new_title)

    draft_path: str = f"{base_path}.article_service.get_draft_by_id"
    update_path: str = f"{base_path}.article_service.update_draft_in_db"

    draft_patch: AsyncMock = patch(draft_path, new_callable=AsyncMock).start()
    draft_update_patch: AsyncMock = patch(update_path, new_callable=AsyncMock).start()

    draft_patch.return_value = fake_draft

    draft = await article_service_v1.update_draft(
        curr_user, refresh_token, draft_update, draft_id, get_session
    )

    draft_patch.stop()
    draft_update_patch.stop()

    assert draft

    verify_token.assert_awaited_once()
    draft_patch.assert_awaited_once()
    draft_update_patch.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_rating(verify_token: AsyncMock, get_session: AsyncClientSession):
    curr_user: UserV1 = fake_user
    refresh_token: str = "fake-refresh-token"

    article_rating: Decimal = Decimal(7.7)
    article_id: PydanticObjectId = PydanticObjectId()

    article_path: str = f"{base_path}.article_service.get_article_by_id"
    rating_path: str = f"{base_path}.article_service.update_rating"

    article_patch: AsyncMock = patch(article_path, new_callable=AsyncMock).start()
    rating_patch: AsyncMock = patch(rating_path, new_callable=AsyncMock).start()

    article_patch.return_value = fake_article

    article = await article_service_v1.update_article_rating(
        curr_user, refresh_token, article_id, article_rating, get_session
    )

    article_patch.stop()
    rating_patch.stop()

    assert article

    verify_token.assert_awaited_once()
    article_patch.assert_awaited_once()
    rating_patch.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_article(verify_token: AsyncMock, get_session: AsyncClientSession):
    curr_user: AdminV1 = fake_admin
    refresh_token: str = "fake-refresh-token"

    article_id: PydanticObjectId = PydanticObjectId()

    article_path: str = f"{base_path}.article_service.get_article_by_id"
    delete_path: str = f"{base_path}.article_service.delete_article_from_db"

    article_patch: AsyncMock = patch(article_path, new_callable=AsyncMock).start()
    delete_patch: AsyncMock = patch(delete_path, new_callable=AsyncMock).start()

    article_patch.return_value = fake_article

    await article_service_v1.delete_article(
        curr_user, refresh_token, article_id, get_session
    )

    article_patch.stop()
    delete_patch.stop()

    verify_token.assert_awaited_once()
    article_patch.assert_awaited_once()
    delete_patch.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_draft(verify_token: AsyncMock, get_session: AsyncClientSession):
    curr_user: AuthorV1 = fake_author
    refresh_token: str = "fake-refresh-token"

    draft_id: PydanticObjectId = PydanticObjectId()

    draft_path: str = f"{base_path}.article_service.get_draft_by_id"
    delete_path: str = f"{base_path}.article_service.delete_draft_from_db"

    draft_patch: AsyncMock = patch(draft_path, new_callable=AsyncMock).start()
    delete_patch: AsyncMock = patch(delete_path, new_callable=AsyncMock).start()

    draft_patch.return_value = fake_draft

    await article_service_v1.delete_draft(
        curr_user, refresh_token, draft_id, get_session
    )

    draft_patch.stop()
    delete_patch.stop()

    verify_token.assert_awaited_once()
    draft_patch.assert_awaited_once()
    delete_patch.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_rating(verify_token: AsyncMock, get_session: AsyncClientSession):
    curr_user: UserV1 = fake_user_1
    refresh_token: str = "fake-refresh-token"

    article_id: PydanticObjectId = PydanticObjectId()

    article_path: str = f"{base_path}.article_service.get_article_by_id"
    delete_path: str = f"{base_path}.article_service.delete_rating_from_db"

    article_patch: AsyncMock = patch(article_path, new_callable=AsyncMock).start()
    delete_patch: AsyncMock = patch(delete_path, new_callable=AsyncMock).start()

    article_patch.return_value = fake_article_with_rating

    await article_service_v1.delete_rating(
        curr_user, refresh_token, article_id, get_session
    )

    article_patch.stop()
    delete_patch.stop()

    verify_token.assert_awaited_once()
    article_patch.assert_awaited_once()
    delete_patch.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_article_images(
    verify_token: AsyncMock, get_session: AsyncClientSession
):
    curr_user: AdminV1 = fake_admin
    refresh_token: str = "fake-refresh-token"

    article_id: PydanticObjectId = PydanticObjectId()

    article_path: str = f"{base_path}.article_service.get_article_by_id"
    delete_path: str = f"{base_path}.article_service.delete_rating_from_db"

    article_patch: AsyncMock = patch(article_path, new_callable=AsyncMock).start()
    delete_patch: AsyncMock = patch(delete_path, new_callable=AsyncMock).start()

    article_patch.return_value = fake_article

    await article_service_v1.delete_article_images(
        curr_user, refresh_token, article_id, get_session
    )

    article_patch.stop()
    delete_patch.stop()

    verify_token.assert_awaited_once()
    article_patch.assert_awaited_once()
    delete_patch.assert_awaited_once()
