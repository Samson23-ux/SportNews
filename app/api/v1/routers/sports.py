from typing import Annotated
from fastapi import APIRouter, Depends, Request, Query
from pymongo.asynchronous.client_session import AsyncClientSession


from app.api.v1.schemas.users import AccountV1
from app.dependencies import get_session, get_current_user
from app.api.v1.schemas.sports import (
    SportResponseV1,
    TeamResponseV1,
    CompetitionResponseV1,
)


sports_router_v1 = APIRouter()


@sports_router_v1.get(
    "/sports",
    status_code=200,
    response_model=SportResponseV1,
    description="Get all sports",
)
async def get_all_sports(
    request: Request,
    curr_user: Annotated[AccountV1, Depends(get_current_user)],
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass


@sports_router_v1.get(
    "/sports/{sport_name}/teams",
    status_code=200,
    response_model=TeamResponseV1,
    description="Get sport teams",
)
async def get_sports_teams(
    sport_name: str,
    request: Request,
    curr_user: Annotated[AccountV1, Depends(get_current_user)],
    session: Annotated[AsyncClientSession, Depends(get_session)],
    cursor: Annotated[str, Query(description="")] = None,
    offset: Annotated[int, Query(description="Limit teams to view at once")] = 20,
):
    pass


@sports_router_v1.get(
    "/sports/{sport_name}/competitions",
    status_code=200,
    response_model=CompetitionResponseV1,
    description="Get sport competitions",
)
async def get_sport_competitions(
    sport_name: str,
    request: Request,
    curr_user: Annotated[AccountV1, Depends(get_current_user)],
    session: Annotated[AsyncClientSession, Depends(get_session)],
    cursor: Annotated[str, Query(description="")] = None,
    offset: Annotated[
        int, Query(description="Limit competitions to view at once")
    ] = 20,
):
    pass
