from beanie import PydanticObjectId
from pymongo.asynchronous.client_session import AsyncClientSession


from app.api.v1.schemas.users import EditorV1, WriterSettingsUpdateV1


class EditorServiceV1:
    async def get_editor_articles(
        self,
        curr_user: EditorV1,
        refresh_token: str,
        session: AsyncClientSession,
        cursor: str = None,
        offset: int = 20,
        sort: str = None,
        order: str = None,
    ):
        pass

    async def get_editor_dashboard(
        self, curr_user: EditorV1, refresh_token: str, session: AsyncClientSession
    ):
        pass

    async def get_editor_profile(
        self,
        curr_user: EditorV1,
        refresh_token: str,
        session: AsyncClientSession,
    ):
        pass

    async def get_editor_profile_settings(
        self,
        curr_user: EditorV1,
        refresh_token: str,
        article_id: PydanticObjectId,
        session: AsyncClientSession,
    ):
        pass

    async def mark_article_edited(
        self, curr_user: EditorV1, refresh_token: str, session: AsyncClientSession
    ):
        pass

    async def update_editor_profile_settings(
        self,
        curr_user: EditorV1,
        refresh_token: str,
        settings_upadate: WriterSettingsUpdateV1,
        session: AsyncClientSession,
    ):
        pass


editor_service_v1 = EditorServiceV1()
