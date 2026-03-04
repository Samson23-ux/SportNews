from beanie import PydanticObjectId
from pymongo.asynchronous.client_session import AsyncClientSession


from app.api.v1.schemas.auth import RefreshTokenV1
from app.api.v1.schemas.users import UserCreateV1, AccountV1


class AuthServiceV1:
    async def get_tokens(self, email: str):
        pass

    async def invalidate_token(
        self, token: RefreshTokenV1, session: AsyncClientSession
    ):
        pass

    async def create_user(self, user_create: UserCreateV1, session: AsyncClientSession):
        pass

    async def sign_in(self, email: str, password: str, session: AsyncClientSession):
        pass

    async def resend_email_code(
        self, user_id: PydanticObjectId, session: AsyncClientSession
    ):
        pass

    async def create_new_token(self, refresh_token: str, session: AsyncClientSession):
        pass

    async def verify_user(self, code: str, session: AsyncClientSession):
        pass

    async def sign_out(
        self, curr_user: AccountV1, refresh_token: str, session: AsyncClientSession
    ):
        pass

    async def update_password(
        self,
        curr_user: AccountV1,
        refresh_token: str,
        curr_password: str,
        new_password: str,
        session: AsyncClientSession,
    ):
        pass

    async def reset_password(
        self, email: str, password: str, session: AsyncClientSession
    ):
        pass

    async def delete_user(
        self,
        curr_user: AccountV1,
        refresh_token: str,
        password: str,
        session: AsyncClientSession,
    ):
        pass


auth_service_v1 = AuthServiceV1()
