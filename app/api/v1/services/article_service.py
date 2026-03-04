from beanie import PydanticObjectId
from pymongo.asynchronous.client_session import AsyncClientSession


class ArticleServiceV1:
    async def get_article_by_id(
        self,
        article_id: PydanticObjectId,
        session: AsyncClientSession,
        refresh_token: str = None,
    ):
        pass

    async def update_article(
        self, session: AsyncClientSession, refresh_token: str = None
    ):
        """
        if refresh_token is None then the update article
        repo should be called. The function assumes another
        service is calling for an article update
        """
        pass
