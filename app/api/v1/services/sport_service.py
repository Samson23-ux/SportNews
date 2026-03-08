from typing import Optional
from pymongo.asynchronous.client_session import AsyncClientSession


from app.api.v1.schemas.users import AccountV1


class SportServicev1:
    async def get_all_sports(
        self,
        curr_user: AccountV1,
        session: AsyncClientSession,
        refresh_token: Optional[str] = None,
    ):
        pass

    async def get_sport_teams(
        self,
        sport_name: str,
        curr_user: AccountV1,
        refresh_token: str,
        session: AsyncClientSession,
        cursor: Optional[str] = None,
        offset: Optional[int] = 20,
    ):
        pass

    async def get_sport_competitions(
        self,
        sport_name: str,
        curr_user: AccountV1,
        refresh_token: str,
        session: AsyncClientSession,
        cursor: Optional[str] = None,
        offset: Optional[int] = 20,
    ):
        pass

    # used by create_article in article_service
    async def get_sport_by_name(self, name: str, session: AsyncClientSession):
        pass


sport_service_v1 = SportServicev1()
