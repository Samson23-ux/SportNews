from typing import Annotated
from fastapi import APIRouter, Depends, Request
from pymongo.asynchronous.client_session import AsyncClientSession


from app.dependencies import get_session, required_roles
from app.api.v1.schemas.users import (
    AccountV1,
    UserRoleV1,
    UserResponseV1,
    SettingsResponseV1,
    UserSettingsUpdateV1,
)


users_router_v1 = APIRouter()


@users_router_v1.get(
    "/users/me",
    status_code=200,
    response_model=UserResponseV1,
    description="Get current user profile",
)
async def get_user_profile(
    request: Request,
    curr_user: Annotated[AccountV1, Depends(required_roles([UserRoleV1.USER]))],
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass


@users_router_v1.get(
    "/users/me/settings",
    status_code=200,
    response_model=SettingsResponseV1,
    description="Get current user profile settings",
)
async def get_user_profile_settings(
    request: Request,
    curr_user: Annotated[AccountV1, Depends(required_roles([UserRoleV1.USER]))],
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass


@users_router_v1.patch(
    "/users/me/settings",
    status_code=200,
    response_model=SettingsResponseV1,
    description="Update user profile settings",
)
async def update_user_profile_settings(
    request: Request,
    settings_update: UserSettingsUpdateV1,
    curr_user: Annotated[AccountV1, Depends(required_roles([UserRoleV1.USER]))],
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass
