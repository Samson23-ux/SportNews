from typing import Optional
from decimal import Decimal
from fastapi import UploadFile
from beanie import PydanticObjectId
from pymongo.asynchronous.client_session import AsyncClientSession


from app.api.v1.schemas.users import UserV1, AccountV1, AuthorV1, EditorV1, AdminV1
from app.api.v1.schemas.articles import (
    ArticleV1,
    ArticleUpdateV1,
    ArticleCreateV1,
    ArticleDraftCreateV1,
)


class ArticleServiceV1:
    async def get_articles(
        self,
        curr_user: AccountV1,
        refresh_token: str,
        session: AsyncClientSession,
        sport: Optional[str] = None,
        cursor: Optional[str] = None,
        offset: Optional[int] = 20,
        sort: Optional[str] = None,
        order: Optional[str] = None,
    ):
        pass

    async def get_article(
        self,
        article_id: PydanticObjectId,
        curr_user: AccountV1,
        session: AsyncClientSession,
        refresh_token: Optional[str] = None,
    ):
        pass

    async def get_draft(
        self,
        draft_id: PydanticObjectId,
        curr_user: AuthorV1 | EditorV1,
        refresh_token: str,
        session: AsyncClientSession,
    ):
        pass

    async def get_drafts(
        self,
        curr_user: AuthorV1 | EditorV1,
        refresh_token: str,
        session: AsyncClientSession,
        cursor: Optional[str] = None,
        offset: Optional[int] = 20,
        sort: Optional[str] = None,
        order: Optional[str] = None,
    ):
        pass

    async def get_article_images(
        self,
        curr_user: AccountV1,
        refresh_token: str,
        article_id: PydanticObjectId,
        session: AsyncClientSession,
    ):
        pass

    async def create_article(
        self,
        curr_user: AuthorV1,
        refresh_token: str,
        article_create: ArticleCreateV1,
        session: AsyncClientSession,
    ):
        pass

    async def create_article_rating(
        self,
        curr_user: UserV1,
        refresh_token: str,
        article_id: PydanticObjectId,
        rating: Decimal,
        session: AsyncClientSession,
    ):
        pass

    async def create_draft(
        self,
        curr_user: AuthorV1 | EditorV1,
        refresh_token: str,
        draft_create: ArticleDraftCreateV1,
        session: AsyncClientSession,
    ):
        pass

    async def upload_article_images(
        self,
        curr_user: AuthorV1 | EditorV1,
        refresh_token: str,
        article_id: PydanticObjectId,
        article_images: list[UploadFile],
        session: AsyncClientSession,
    ):
        pass

    async def update_article(
        self,
        curr_user: EditorV1,
        article_update: ArticleUpdateV1,
        article_id: PydanticObjectId,
        session: AsyncClientSession,
        refresh_token: Optional[str] = None,
    ):
        pass

    async def update_draft(
        self,
        curr_user: AuthorV1 | EditorV1,
        refresh_token: str,
        draft_update: ArticleDraftCreateV1,
        draft_id: PydanticObjectId,
        session: AsyncClientSession,
    ):
        pass

    async def mark_article_edited(
        self,
        article_id: PydanticObjectId,
        article: ArticleV1,
        session: AsyncClientSession,
    ):
        pass

    async def update_article_rating(
        self,
        curr_user: UserV1,
        refresh_token: str,
        article_id: PydanticObjectId,
        rating: Decimal,
        session: AsyncClientSession,
    ):
        "the article must have been rated by the user"

    async def delete_article(
        self,
        curr_user: AdminV1,
        refresh_token: str,
        article_id: PydanticObjectId,
        session: AsyncClientSession,
    ):
        pass

    async def delete_draft(
        self,
        curr_user: AuthorV1 | EditorV1,
        refresh_token: str,
        draft_id: PydanticObjectId,
        session: AsyncClientSession,
    ):
        pass

    async def delete_rating(
        self,
        curr_user: UserV1,
        refresh_token: str,
        article_id: PydanticObjectId,
        session: AsyncClientSession,
    ):
        pass

    async def delete_article_images(
        self,
        curr_user: UserV1,
        refresh_token: str,
        article_id: PydanticObjectId,
        session: AsyncClientSession,
    ):
        pass


article_service_v1 = ArticleServiceV1()
