from pymongo.asynchronous.client_session import AsyncClientSession


class AuthorRepoV1():
    async def get_articles_from_db(self, session: AsyncClientSession):
        pass

    async def get_dashboard_from_db(self, session: AsyncClientSession):
        pass

    async def update_author_in_db(self, session: AsyncClientSession):
        pass


author_repo_v1 = AuthorRepoV1()
