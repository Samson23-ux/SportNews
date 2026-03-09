from beanie import Document
from beanie import init_beanie


from app.core.config import settings
from app.database.models import db_models
from app.database.client import mongo_client
from app.api.v1.schemas.users import UserRoleV1


async def get_session():
    db_name: str = settings.DB_NAME
    db = mongo_client[db_name]
    models: list[Document] = db_models

    await init_beanie(db, document_models=models, allow_index_dropping=True)

    """
    enable session for casual consistency, retryable writes and transaction
    support
    """
    async with mongo_client.start_session(causal_consistency=True) as session:
        yield session


async def get_current_user():
    pass


def required_roles(roles: list[UserRoleV1]):
    async def role_checker():
        pass

    return role_checker
