from typing import Annotated
from beanie import PydanticObjectId
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, Request, Form, Response
from pymongo.asynchronous.client_session import AsyncClientSession


from app.core.security import oauth
from app.api.v1.schemas.auth import TokenV1
from app.dependencies import get_session, get_current_user
from app.api.v1.schemas.users import (
    UserResponseV1,
    UserCreateV1,
    AccountV1,
    PasswordUpdateV1,
)


auth_router_v1 = APIRouter()


@auth_router_v1.post(
    "/auth/sign-up",
    status_code=201,
    response_model=UserResponseV1,
    description="Create user account",
)
async def sign_up(
    sign_up_data: UserCreateV1,
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass


@auth_router_v1.post(
    "/auth/{user_id}/resend-code",
    status_code=201,
    response_model=UserResponseV1,
    description="Request for a new verification code",
)
async def resend_email_code(
    user_id: PydanticObjectId,
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass


@auth_router_v1.post(
    "/auth/sign-in",
    status_code=201,
    response_model=TokenV1,
    description="Sign in with email and password",
)
async def sign_in(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass


@auth_router_v1.get(
    "/auth/sign-in/google",
    status_code=302,
    response_model=TokenV1,
    description="Sign in Google account",
)
async def sign_in_with_google(
    request: Request,
):
    pass


@auth_router_v1.post(
    "/auth/callback",
    status_code=201,
    response_model=TokenV1,
    description="Callback URL for Google OAuth2",
)
async def create_user(
    response: Response,
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass


@auth_router_v1.post(
    "/auth/refresh",
    status_code=201,
    response_model=TokenV1,
    description="Create new access token for user with a valid refresh token",
)
async def create_new_token(
    request: Request,
    response: Response,
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass


@auth_router_v1.patch(
    "/auth/verify/{code}",
    status_code=200,
    response_model=UserResponseV1,
    description="Verify user account",
)
async def verify_account(
    code: str,
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass


@auth_router_v1.patch(
    "/auth/sign-out",
    status_code=200,
    description="Sign out user account",
)
async def sign_out(
    request: Request,
    curr_user: Annotated[AccountV1, Depends(get_current_user)],
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass


@auth_router_v1.patch(
    "/auth/update-password",
    status_code=200,
    response_model=UserResponseV1,
    description="Update user password",
)
async def update_password(
    request: Request,
    password_update: PasswordUpdateV1,
    curr_user: Annotated[AccountV1, Depends(get_current_user)],
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass


@auth_router_v1.patch(
    "/auth/reset-password",
    status_code=200,
    response_model=UserResponseV1,
    description="Reset user password",
)
async def reset_password(
    email: Annotated[str, Form(..., description="Input user email")],
    password: Annotated[str, Form(..., description="Input new password")],
    session: Annotated[AsyncClientSession, Depends(get_session)],
):
    pass


@auth_router_v1.delete(
    "/auth/",
    status_code=204,
    description="Delete account permanently"
)
async def delete_account(
    request: Request,
    password: Annotated[str, Form(..., description="Input user password")],
    curr_user: Annotated[AccountV1, Depends(get_current_user)],
    session: Annotated[AsyncClientSession, Depends(get_session)]
):
    pass
