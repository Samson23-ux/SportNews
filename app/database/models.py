from beanie import Document


from app.api.v1.schemas.tasks import TaskV1
from app.api.v1.schemas.auth import RefreshTokenV1, EmailCodeV1
from app.api.v1.schemas.users import (
    UserV1,
    AdminV1,
    AuthorV1,
    EditorV1,
    AccountV1,
    EmployeeV1,
    GoogleUserV1,
    UserWithPasswordV1,
)
from app.api.v1.schemas.articles import (
    ArticleV1,
    TeamSportV1,
    SubscriptionV1,
    ArticleDraftV1,
    IndividualSportV1,
)
from app.api.v1.schemas.sports import (
    GolfV1,
    SportV1,
    TennisV1,
    BoxingV1,
    FootballV1,
    BasketballV1,
)


db_models: list[Document] = [
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
    GoogleUserV1,
    ArticleDraftV1,
    RefreshTokenV1,
    SubscriptionV1,
    IndividualSportV1,
    UserWithPasswordV1,
]
