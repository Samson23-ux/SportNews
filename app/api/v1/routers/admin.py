from typing import Annotated
from datetime import datetime
from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, Request, Query
from pymongo.asynchronous.client_session import AsyncClientSession


from app.api.v1.schemas.sports import SportResponseV1
from app.dependencies import get_session, required_roles
from app.api.v1.schemas.articles import ArticleResponseV1, ArticleStatusV1
from app.api.v1.schemas.users import (
    AccountV1,
    UserRoleV1,
    AuthorCreateV1,
    EditorCreateV1,
    UserResponseV1,
    AdminResponseV1,
    WriterResponseV1,
    SettingsResponseV1,
    EmployeeSettingsV1,
    DashboardResponseV1,
)


admin_router_v1 = APIRouter()


@admin_router_v1.get(
    "/admin/me",
    status_code=200,
    response_model=AdminResponseV1,
    description="Get current admin profile",
)
async def get_admin_profile(
    request: Request,
    curr_user: Annotated[AccountV1, Depends(required_roles([UserRoleV1.ADMIN]))],
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass


@admin_router_v1.get(
    "/admin/me/settings",
    status_code=200,
    response_model=SettingsResponseV1,
    description="Get current admin profile settings",
)
async def get_admin_profile_settings(
    request: Request,
    curr_user: Annotated[AccountV1, Depends(required_roles([UserRoleV1.ADMIN]))],
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass


@admin_router_v1.get(
    "/admin/me/analytics/dashboard",
    status_code=200,
    response_model=DashboardResponseV1,
    description="Get current admin dashboard analytics",
)
async def get_admin_dashboard(
    request: Request,
    curr_user: Annotated[AccountV1, Depends(required_roles([UserRoleV1.ADMIN]))],
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass


@admin_router_v1.get(
    "/admin/users",
    status_code=200,
    response_model=UserResponseV1,
    description="Get all users",
)
async def get_all_users(
    request: Request,
    curr_user: Annotated[AccountV1, Depends(required_roles([UserRoleV1.ADMIN]))],
    session: Annotated[AsyncClientSession, Depends(get_session)],
    cursor: Annotated[str, Query(description="")] = None,
    offset: Annotated[int, Query(description="Limit users to view at once")] = 20,
    sort: Annotated[str, Query(description="Sort users by created_at")] = None,
    order: Annotated[str, Query(description="Sort users in asc or desc order")] = None,
):
    pass


@admin_router_v1.get(
    "/admin/authors",
    status_code=200,
    response_model=WriterResponseV1,
    description="Get all authors",
)
async def get_all_authors(
    request: Request,
    curr_user: Annotated[AccountV1, Depends(required_roles([UserRoleV1.ADMIN]))],
    session: Annotated[AsyncClientSession, Depends(get_session)],
    cursor: Annotated[str, Query(description="")] = None,
    offset: Annotated[int, Query(description="Limit users to view at once")] = 20,
    sort: Annotated[str, Query(description="Sort users by created_at")] = None,
    order: Annotated[str, Query(description="Sort users in asc or desc order")] = None,
):
    pass


@admin_router_v1.get(
    "/admin/editors",
    status_code=200,
    response_model=WriterResponseV1,
    description="Get all editors",
)
async def get_all_editors(
    request: Request,
    curr_user: Annotated[AccountV1, Depends(required_roles([UserRoleV1.ADMIN]))],
    session: Annotated[AsyncClientSession, Depends(get_session)],
    cursor: Annotated[str, Query(description="")] = None,
    offset: Annotated[int, Query(description="Limit users to view at once")] = 20,
    sort: Annotated[str, Query(description="Sort users by created_at")] = None,
    order: Annotated[str, Query(description="Sort users in asc or desc order")] = None,
):
    pass


@admin_router_v1.get(
    "/admin/articles",
    status_code=200,
    response_model=ArticleResponseV1,
    description="Get all articles",
)
async def get_all_articles(
    request: Request,
    curr_user: Annotated[AccountV1, Depends(required_roles([UserRoleV1.ADMIN]))],
    session: Annotated[AsyncClientSession, Depends(get_session)],
    sport: Annotated[str, Query(description="Filter articles by sport")] = None,
    status: Annotated[
        ArticleStatusV1, Query(description="Filter by article status")
    ] = None,
    cursor: Annotated[str, Query(description="")] = None,
    offset: Annotated[int, Query(description="Limit users to view at once")] = 20,
    sort: Annotated[str, Query(description="Sort users by created_at")] = None,
    order: Annotated[str, Query(description="Sort users in asc or desc order")] = None,
):
    pass


@admin_router_v1.get(
    "/admin/articles/readers",
    status_code=200,
    response_model=ArticleResponseV1,
    description="Get all articles readers",
)
async def get_article_readers(
    request: Request,
    curr_user: Annotated[AccountV1, Depends(required_roles([UserRoleV1.ADMIN]))],
    session: Annotated[AsyncClientSession, Depends(get_session)],
    start_date: Annotated[
        datetime, Query(description="Set start date to view readers from")
    ] = None,
    end_date: Annotated[
        datetime, Query(description="Set end date to view readers to")
    ] = None,
):
    pass


@admin_router_v1.get(
    "/admin/sports",
    status_code=200,
    response_model=SportResponseV1,
    description="Get all sport categories",
)
async def get_all_sports(
    request: Request,
    curr_user: Annotated[AccountV1, Depends(required_roles([UserRoleV1.ADMIN]))],
    session: Annotated[AsyncClientSession, Depends(get_session)],
    cursor: Annotated[str, Query(description="")] = None,
    offset: Annotated[int, Query(description="Limit users to view at once")] = 20,
):
    pass


@admin_router_v1.post(
    "/admin/editors/{editor_id}/articles/{article_id}/assign",
    status_code=201,
    response_model=ArticleResponseV1,
    description="Assign article to editor for edit",
)
async def assign_article(
    editor_id: PydanticObjectId,
    article_id: PydanticObjectId,
    curr_user: Annotated[AccountV1, Depends(required_roles([UserRoleV1.ADMIN]))],
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass


@admin_router_v1.post(
    "/admin/authors",
    status_code=201,
    response_model=WriterResponseV1,
    description="Assign author role",
)
async def create_author(
    request: Request,
    author_create: AuthorCreateV1,
    curr_user: Annotated[AccountV1, Depends(required_roles([UserRoleV1.ADMIN]))],
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass


@admin_router_v1.post(
    "/admin/editors",
    status_code=201,
    response_model=WriterResponseV1,
    description="Assign editor role",
)
async def create_editor(
    request: Request,
    editor_create: EditorCreateV1,
    curr_user: Annotated[AccountV1, Depends(required_roles([UserRoleV1.ADMIN]))],
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass


@admin_router_v1.post(
    "/admin/info",
    status_code=201,
    response_model=AdminResponseV1,
    description="Send information to users",
)
async def send_information(
    request: Request,
    curr_user: Annotated[AccountV1, Depends(required_roles([UserRoleV1.ADMIN]))],
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass


@admin_router_v1.post(
    "/admin/newsletter",
    status_code=201,
    response_model=AdminResponseV1,
    description="Send newsletter to users",
)
async def send_newsletter(
    request: Request,
    curr_user: Annotated[AccountV1, Depends(required_roles([UserRoleV1.ADMIN]))],
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass


@admin_router_v1.patch(
    "/admin/articles/{article_id}/publish",
    status_code=200,
    response_model=ArticleResponseV1,
    description="Publish article after it has been edited by an editor",
)
async def publish_article(
    article_id: PydanticObjectId,
    request: Request,
    curr_user: Annotated[AccountV1, Depends(required_roles([UserRoleV1.ADMIN]))],
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass


@admin_router_v1.patch(
    "/admin/me/settings",
    status_code=200,
    response_model=SettingsResponseV1,
    description="Update admin profile settings",
)
async def update_admin_profile_settings(
    request: Request,
    settings_update: EmployeeSettingsV1,
    curr_user: Annotated[AccountV1, Depends(required_roles([UserRoleV1.ADMIN]))],
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass


@admin_router_v1.delete(
    "/admin/authors/{author_id}",
    status_code=204,
    description="Remove author role",
)
async def delete_author(
    request: Request,
    author_id: PydanticObjectId,
    curr_user: Annotated[AccountV1, Depends(required_roles([UserRoleV1.ADMIN]))],
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass


@admin_router_v1.delete(
    "/admin/editors/{editor_id}",
    status_code=204,
    description="Remove editor role",
)
async def delete_editor(
    request: Request,
    editor_id: PydanticObjectId,
    curr_user: Annotated[AccountV1, Depends(required_roles([UserRoleV1.ADMIN]))],
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass
