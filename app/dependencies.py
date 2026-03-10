from fastapi import Depends
from beanie import Document
from beanie import init_beanie
from sentry_sdk import logger as sentry_logger
from fastapi.security import OAuth2PasswordBearer
from pymongo.asynchronous.client_session import AsyncClientSession


from app.core.config import settings
from app.database.models import db_models
from app.core.security import decode_token
from app.database.client import mongo_client
from app.api.v1.schemas.users import UserRoleV1, AccountV1
from app.api.v1.services.user_service import user_service_v1
from app.core.exceptions import (
    AuthenticationError,
    AuthorizationError,
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/sign-in/")


async def get_session():
    db_name: str = settings.DB_NAME
    db = mongo_client[db_name]
    models: list[Document] = db_models

    sentry_logger.info("Initializing beanie with document models")
    await init_beanie(db, document_models=models, allow_index_dropping=True)
    sentry_logger.info("Database collections initialized")

    """
    enable session for casual consistency, retryable writes and transaction
    support
    """

    sentry_logger.info("Database session started...")
    async with mongo_client.start_session(causal_consistency=True) as session:
        yield session
    sentry_logger.info("Database session ended...")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncClientSession = Depends(get_session),
):
    key: str = settings.ACCESS_TOKEN_SECRET_KEY
    payload: dict = await decode_token(token, key)

    if not payload:
        sentry_logger.error("User not authenticated")
        raise AuthenticationError()

    user_email: str = payload.get("sub")

    user: AccountV1 = await user_service_v1.get_user_by_email(user_email, session)

    return user


def required_roles(roles: list[UserRoleV1]):
    async def role_checker(curr_user: AccountV1 = Depends(get_current_user)):
        if curr_user.role not in roles:
            sentry_logger.error("User {id} is not authorized", id=curr_user.id)
            raise AuthorizationError()
        return curr_user

    return role_checker
