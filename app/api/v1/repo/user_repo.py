from pymongo.asynchronous.client_session import AsyncClientSession


class UserRepoV1:
    async def add_user_to_db(self, session: AsyncClientSession):
        pass

    async def get_user_by_email(self, session: AsyncClientSession):
        pass

    async def get_user_by_id(self, session: AsyncClientSession):
        pass

    async def update_user_in_db(self, session: AsyncClientSession):
        pass

    async def delete_user_from_db(self, session: AsyncClientSession):
        pass


user_repo_v1 = UserRepoV1()
