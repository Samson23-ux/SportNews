from pymongo.asynchronous.client_session import AsyncClientSession


class EditorRepoV1():
    async def get_articles_from_db(self, session: AsyncClientSession):
        pass

    async def get_dashboard_from_db(self, session: AsyncClientSession):
        pass

    async def update_editor_in_db(self, session: AsyncClientSession):
        pass


editor_repo_v1 = EditorRepoV1()
