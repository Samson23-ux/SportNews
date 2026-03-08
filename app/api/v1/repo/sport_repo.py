from pymongo.asynchronous.client_session import AsyncClientSession


class SportRepoV1:
    async def get_all_sports(self, session: AsyncClientSession):
        pass

    async def get_sport_teams(self, session: AsyncClientSession):
        pass

    async def get_sport_competitions(self, session: AsyncClientSession):
        pass

    # used by create_article in article_service
    async def get_sport_by_name(self, session: AsyncClientSession):
        pass


sport_repo_v1 = SportRepoV1()
