from beanie import PydanticObjectId
from pymongo.asynchronous.client_session import AsyncClientSession


from app.api.v1.schemas.users import UserV1, UserSettingsUpdateV1


class UserServiceV1:
    async def create_user(self, user: UserV1, session: AsyncClientSession):
        pass

    async def get_user_by_email(
        self,
        email: str,
        session: AsyncClientSession,
        refresh_token: str = None,
    ):
        pass

    async def get_user_by_id(
        self,
        user_id: PydanticObjectId,
        session: AsyncClientSession,
        refresh_token: str = None,
    ):
        pass

    async def get_user_profile(
        self, curr_user: UserV1, refresh_token: str, session: AsyncClientSession
    ):
        pass

    async def get_user_profile_settings(
        self, curr_user: UserV1, refresh_token: str, session: AsyncClientSession
    ):
        pass

    async def update_user(
        self,
        curr_user: UserV1,
        session: AsyncClientSession,
        refresh_token: str = None,
    ):
        pass

    async def update_user_profile_settings(
        self,
        curr_user: UserV1,
        refresh_token: str,
        settings_upadate: UserSettingsUpdateV1,
        session: AsyncClientSession,
    ):
        pass

    async def delete_user(
        self,
        curr_user: UserV1,
        session: AsyncClientSession,
        refresh_token: str = None,
    ):
        pass


user_service_v1 = UserServiceV1()
