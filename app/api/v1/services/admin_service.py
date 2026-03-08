from typing import Optional
from datetime import datetime
from beanie import PydanticObjectId
from pymongo.asynchronous.client_session import AsyncClientSession


from app.api.v1.schemas.users import (
    AdminV1,
    AuthorCreateV1,
    EditorCreateV1,
    EmployeeSettingsV1,
)


class AdminServicev1:
    async def get_admin_profile(
        self, curr_user: AdminV1, refresh_token: str, session: AsyncClientSession
    ):
        pass

    async def get_admin_profile_settings(
        self, curr_user: AdminV1, refresh_token: str, session: AsyncClientSession
    ):
        pass

    async def get_admin_dashboard(
        self, curr_user: AdminV1, refresh_token: str, session: AsyncClientSession
    ):
        pass

    async def get_all_users(
        self,
        curr_user: AdminV1,
        refresh_token: str,
        session: AsyncClientSession,
        cursor: Optional[str] = None,
        offset: Optional[int] = 20,
        sort: Optional[str] = None,
        order: Optional[str] = None,
    ):
        pass

    async def get_all_authors(
        self,
        curr_user: AdminV1,
        refresh_token: str,
        session: AsyncClientSession,
        cursor: Optional[str] = None,
        offset: Optional[int] = 20,
        sort: Optional[str] = None,
        order: Optional[str] = None,
    ):
        pass

    async def get_all_editors(
        self,
        curr_user: AdminV1,
        refresh_token: str,
        session: AsyncClientSession,
        cursor: Optional[str] = None,
        offset: Optional[int] = 20,
        sort: Optional[str] = None,
        order: Optional[str] = None,
    ):
        pass

    async def get_all_articles(
        self,
        curr_user: AdminV1,
        refresh_token: str,
        session: AsyncClientSession,
        sport: Optional[str] = None,
        status: Optional[str] = None,
        cursor: Optional[str] = None,
        offset: Optional[int] = 20,
        sort: Optional[str] = None,
        order: Optional[str] = None,
    ):
        pass

    async def get_article_readers(
        self,
        curr_user: AdminV1,
        refresh_token: str,
        session: AsyncClientSession,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ):
        pass

    async def get_all_sports(
        self,
        curr_user: AdminV1,
        refresh_token: str,
        session: AsyncClientSession,
    ):
        pass

    async def assign_article(
        self,
        editor_id: PydanticObjectId,
        article_id: PydanticObjectId,
        curr_user: AdminV1,
        refresh_token: str,
        session: AsyncClientSession,
    ):
        pass

    async def create_author(
        self,
        user_id: PydanticObjectId,
        author_create: AuthorCreateV1,
        curr_user: AdminV1,
        refresh_token: str,
        session: AsyncClientSession,
    ):
        pass

    async def create_editor(
        self,
        user_id: PydanticObjectId,
        editor_create: EditorCreateV1,
        curr_user: AdminV1,
        refresh_token: str,
        session: AsyncClientSession,
    ):
        pass

    async def send_information(
        self,
        curr_user: AdminV1,
        refresh_token: str,
        session: AsyncClientSession,
    ):
        pass

    async def send_newsletter(
        self,
        curr_user: AdminV1,
        refresh_token: str,
        session: AsyncClientSession,
    ):
        pass

    async def publish_article(
        self,
        article_id: PydanticObjectId,
        curr_user: AdminV1,
        refresh_token: str,
        session: AsyncClientSession,
    ):
        pass

    async def update_admin_profile_settings(
        self,
        curr_user: AdminV1,
        refresh_token: str,
        settings_upadate: EmployeeSettingsV1,
        session: AsyncClientSession,
    ):
        pass

    async def delete_author(
        self,
        author_id: PydanticObjectId,
        curr_user: AdminV1,
        refresh_token: str,
        session: AsyncClientSession,
    ):
        pass

    async def delete_editor(
        self,
        editor_id: PydanticObjectId,
        curr_user: AdminV1,
        refresh_token: str,
        session: AsyncClientSession,
    ):
        pass


admin_service_v1 = AdminServicev1()
