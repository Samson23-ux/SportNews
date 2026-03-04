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
    cursor: Annotated[str, Query(default=None, description="")],
    offset: Annotated[
        int, Query(default=20, description="Limit sports to view at once")
    ],
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
    cursor: Annotated[str, Query(default=None, description="")],
    offset: Annotated[
        int, Query(default=20, description="Limit teams to view at once")
    ],
    curr_user: Annotated[AccountV1, Depends(get_current_user)],
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass


@sports_router_v1.get(
    "/sports/{sport_name}/competitions",
    status_code=200,
    response_model=CompetitionResponseV1,
    description="Get sport competitions",
)
async def get_sports_competition(
    sport_name: str,
    request: Request,
    cursor: Annotated[str, Query(default=None, description="")],
    offset: Annotated[
        int, Query(default=20, description="Limit competitions to view at once")
    ],
    curr_user: Annotated[AccountV1, Depends(get_current_user)],
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass
