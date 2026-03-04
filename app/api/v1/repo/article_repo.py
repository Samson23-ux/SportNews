from pymongo.asynchronous.client_session import AsyncClientSession


class ArticleRepoV1:
    async def get_article_by_id(self, session: AsyncClientSession):
        pass

    async def update_article_in_db(self, session: AsyncClientSession):
        pass


article_repo_v1 = ArticleRepoV1()
