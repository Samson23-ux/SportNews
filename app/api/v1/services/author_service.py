from pymongo.asynchronous.client_session import AsyncClientSession


from app.api.v1.schemas.users import AuthorV1, WriterSettingsUpdateV1


class AuthorServiceV1:
    async def get_author_articles(
        self,
        curr_user: AuthorV1,
        refresh_token: str,
        session: AsyncClientSession,
        cursor: str = None,
        offset: int = 20,
        sort: str = None,
        order: str = None,
    ):
        pass

    async def get_author_dashboard(
        self, curr_user: AuthorV1, refresh_token: str, session: AsyncClientSession
    ):
        pass

    async def get_author_profile(
        self, curr_user: AuthorV1, refresh_token: str, session: AsyncClientSession
    ):
        pass

    async def get_author_profile_settings(
        self, curr_user: AuthorV1, refresh_token: str, session: AsyncClientSession
    ):
        pass

    async def update_author_profile_settings(
        self,
        curr_user: AuthorV1,
        refresh_token: str,
        settings_upadate: WriterSettingsUpdateV1,
        session: AsyncClientSession,
    ):
        pass


author_service_v1 = AuthorServiceV1()
