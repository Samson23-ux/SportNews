from pymongo.asynchronous.client_session import AsyncClientSession


class AuthRepoV1:
    async def get_refresh_token(self, session: AsyncClientSession):
        pass

    async def add_code_to_db(self, session: AsyncClientSession):
        pass

    async def add_tokens_to_db(self, session: AsyncClientSession):
        pass

    async def update_tokens(self, session: AsyncClientSession):
        pass

    async def get_verification_code(self, session: AsyncClientSession):
        pass


auth_repo_v1 = AuthRepoV1()
