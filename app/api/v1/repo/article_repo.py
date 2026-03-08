from pymongo.asynchronous.client_session import AsyncClientSession


class ArticleRepoV1:
    async def get_articles(self, session: AsyncClientSession):
        pass

    async def get_drafts(self, session: AsyncClientSession):
        pass

    async def get_article_by_id(self, session: AsyncClientSession):
        pass

    async def get_draft_by_id(self, session: AsyncClientSession):
        pass

    async def get_article_images(self, session: AsyncClientSession):
        pass

    async def add_article_to_db(self, session: AsyncClientSession):
        pass

    async def create_rating(self, session: AsyncClientSession):
        pass

    async def add_draft_to_db(self, session: AsyncClientSession):
        pass

    async def add_article_image(self, session: AsyncClientSession):
        pass

    async def update_article_in_db(self, session: AsyncClientSession):
        pass

    async def update_draft_in_db(self, session: AsyncClientSession):
        pass

    async def update_rating(self, session: AsyncClientSession):
        pass

    async def delete_article_from_db(self, session: AsyncClientSession):
        pass

    async def delete_draft_from_db(self, session: AsyncClientSession):
        pass

    async def delete_rating_from_db(self, session: AsyncClientSession):
        pass

    async def delete_image_from_db(self, session: AsyncClientSession):
        pass


article_repo_v1 = ArticleRepoV1()
