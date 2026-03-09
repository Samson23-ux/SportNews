from typing import Annotated
from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, Request, Query
from pymongo.asynchronous.client_session import AsyncClientSession


from app.dependencies import get_session, required_roles
from app.api.v1.schemas.articles import ArticleResponseV1
from app.api.v1.schemas.users import (
    UserRoleV1,
    AccountV1,
    WriterResponseV1,
    SettingsResponseV1,
    DashboardResponseV1,
    WriterSettingsUpdateV1,
)


editors_router_v1 = APIRouter()


@editors_router_v1.get(
    "/editors/me/articles",
    status_code=200,
    response_model=ArticleResponseV1,
    description="Get current editor edited articles",
)
async def get_editor_articles(
    request: Request,
    curr_user: Annotated[AccountV1, Depends(required_roles([UserRoleV1.EDITOR]))],
    session: Annotated[AsyncClientSession, Depends(get_session)],
    cursor: Annotated[str, Query(description="")] = None,
    offset: Annotated[int, Query(description="Limit users to view at once")] = 20,
    sort: Annotated[str, Query(description="Sort users by created_at")] = None,
    order: Annotated[str, Query(description="Sort users in asc or desc order")] = None,
):
    pass


@editors_router_v1.get(
    "/editors/me/analytics/dashboard",
    status_code=200,
    response_model=DashboardResponseV1,
    description="Get current editor dashboard analytics",
)
async def get_editor_dashboard(
    request: Request,
    curr_user: Annotated[AccountV1, Depends(required_roles([UserRoleV1.EDITOR]))],
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass


@editors_router_v1.get(
    "/editors/me",
    status_code=200,
    response_model=WriterResponseV1,
    description="Get current editor profile",
)
async def get_editor_profile(
    request: Request,
    curr_user: Annotated[AccountV1, Depends(required_roles([UserRoleV1.EDITOR]))],
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass


@editors_router_v1.get(
    "/editors/me/settings",
    status_code=200,
    response_model=SettingsResponseV1,
    description="Get current editor profile settings",
)
async def get_editor_profile_settings(
    request: Request,
    curr_user: Annotated[AccountV1, Depends(required_roles([UserRoleV1.EDITOR]))],
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass


@editors_router_v1.patch(
    "/editors/articles/{article_id}/edited",
    status_code=200,
    response_model=ArticleResponseV1,
    description="Mark article edited. Editors can only mark assigned articles edited",
)
async def mark_article_edited(
    article_id: PydanticObjectId,
    request: Request,
    curr_user: Annotated[AccountV1, Depends(required_roles([UserRoleV1.EDITOR]))],
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass


@editors_router_v1.patch(
    "/editors/me/settings",
    status_code=200,
    response_model=SettingsResponseV1,
    description="Update editor profile settings",
)
async def update_editor_profile_settings(
    request: Request,
    settings_update: WriterSettingsUpdateV1,
    curr_user: Annotated[AccountV1, Depends(required_roles([UserRoleV1.EDITOR]))],
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass
