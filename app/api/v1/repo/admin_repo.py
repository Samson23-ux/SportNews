from pymongo.asynchronous.client_session import AsyncClientSession


class AdminRepoV1:
    async def get_dashboard_from_db(self, session: AsyncClientSession):
        pass

    async def get_users_from_db(self, session: AsyncClientSession):
        pass

    async def get_authors_from_db(self, session: AsyncClientSession):
        pass

    async def get_editors_from_db(self, session: AsyncClientSession):
        pass

    async def get_articles_from_db(self, session: AsyncClientSession):
        pass

    async def get_article_readers(self, session: AsyncClientSession):
        pass

    async def assign_article(self, session: AsyncClientSession):
        pass

    async def add_author_to_db(self, session: AsyncClientSession):
        pass

    async def add_editor_to_db(self, session: AsyncClientSession):
        pass

    async def update_admin_in_db(self, session: AsyncClientSession):
        pass

    async def delete_author_from_db(self, session: AsyncClientSession):
        pass

    async def delete_editor_from_db(self, session: AsyncClientSession):
        pass


admin_repo_v1 = AdminRepoV1()
