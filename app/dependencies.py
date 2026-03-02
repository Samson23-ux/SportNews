from beanie import Document
from beanie import init_beanie


from app.database import client
from app.core.config import settings
from app.api.v1.schemas.tasks import TaskV1
from app.api.v1.schemas.users import (
    UserV1,
    AdminV1,
    AuthorV1,
    EditorV1,
    AccountV1,
    EmployeeV1,
    UserRoleV1,
)
from app.api.v1.schemas.auth import RefreshTokenV1, EmailCodeV1
from app.api.v1.schemas.articles import (
    ArticleV1,
    SubscriptionV1,
    TeamSportV1,
    IndividualSportV1,
)
from app.api.v1.schemas.sports import (
    SportV1,
    FootballV1,
    BasketballV1,
    TennisV1,
    GolfV1,
    BoxingV1,
)


async def get_session():
    db_name: str = settings.DB_NAME
    db = client[db_name]
    models: list[Document] = [
        UserV1,
        GolfV1,
        TaskV1,
        SportV1,
        AdminV1,
        AuthorV1,
        EditorV1,
        BoxingV1,
        TennisV1,
        AccountV1,
        ArticleV1,
        FootballV1,
        EmployeeV1,
        TeamSportV1,
        EmailCodeV1,
        BasketballV1,
        RefreshTokenV1,
        SubscriptionV1,
        IndividualSportV1,
    ]

    await init_beanie(db, document_models=models, allow_index_dropping=True)

    """
    enable session for casual consistency, retryable writes and transaction
    support
    """
    async with client.start_session(causal_consistency=True) as session:
        yield session


async def get_current_user():
    pass


def required_roles(roles: list[UserRoleV1]):
    async def role_checker():
        pass

    return role_checker
