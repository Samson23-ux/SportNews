from enum import Enum
from uuid import UUID
from decimal import Decimal
from beanie import PydanticObjectId
from typing import Optional, Literal
from datetime import datetime, timezone
from pydantic import BaseModel, EmailStr, Field


"""
separate models for unit tests these models inherit directly
from pydantic BaseModel class and does not require beanie
initialization
"""


# sports model
class CompetitionTypeV1(str, Enum):
    LEAGUE = "league"
    EUROPE = "europe"
    TOURNAMENT = "tournament"
    CHAMPIONSHIP = "championship"


class SportEnumv1(str, Enum):
    FOOTBALL = "football"
    BASKETBALL = "basketball"
    TENNIS = "tennis"
    GOLF = "golf"
    BOXING = "boxing"


class SportV1(BaseModel):
    name: str


class TeamV1(BaseModel):
    name: str
    country: str


class CompetitionV1(BaseModel):
    name: str
    type: CompetitionTypeV1


class FootballV1(SportV1):
    teams: list[TeamV1]
    competitions: list[CompetitionV1]


# users model
class UserRoleV1(str, Enum):
    USER = "user"
    ADMIN = "admin"
    AUTHOR = "author"
    EDITOR = "editor"


class Theme(str, Enum):
    DARK = "dark"
    WHITE = "white"


class ProfileSettingsV1(BaseModel):
    timezone: str = "utc"
    theme: Theme = Theme.WHITE


class UserSettingsV1(ProfileSettingsV1):
    favourite_teams: list[TeamV1] = []
    subscribe: bool = False
    receive_infomation: bool = False
    receive_newsletter: bool = False


class EmployeeSettingsV1(ProfileSettingsV1):
    pass


class WriterSettingsV1(EmployeeSettingsV1):
    auto_delete_drafts: bool = False


class AccountV1(BaseModel):
    email: EmailStr
    is_verified: bool = False
    created_at: datetime = datetime.now(timezone.utc)


class GoogleUserV1(AccountV1):
    is_verified: bool = True


class UserWithPasswordV1(AccountV1):
    password: str = Field(min_length=8)


class EmployeeV1(UserWithPasswordV1):
    name: str
    nationality: str
    profile_settings: EmployeeSettingsV1


class AdminV1(EmployeeV1):
    role: UserRoleV1 = UserRoleV1.ADMIN


class EditorV1(EmployeeV1):
    role: UserRoleV1 = UserRoleV1.EDITOR
    tasks: int = 0
    profile_settings: WriterSettingsV1


class AuthorV1(EmployeeV1):
    role: UserRoleV1 = UserRoleV1.AUTHOR
    profile_settings: WriterSettingsV1


class UserV1(UserWithPasswordV1):
    role: UserRoleV1 = UserRoleV1.USER
    profile_settings: UserSettingsV1


class WriterCreateV1(BaseModel):
    name: str
    nationality: str
    user_id: PydanticObjectId


class EditorCreateV1(WriterCreateV1):
    pass


class AuthorCreateV1(WriterCreateV1):
    pass


class EmployeeDashboardV1(BaseModel):
    total_articles: int
    total_article_readers: int
    avg_article_readers: int


class AdminDashboardV1(EmployeeDashboardV1):
    total_users: int
    total_authors: int
    total_editors: int
    total_article_readers: dict[str, int]

    """total_article_readers example -> {
        total_readers: int,
        readers_who_rate: int,
        readers_who_dont_rate: int
    }"""


class WriterDashboardV1(EmployeeDashboardV1):
    total_published_articles: int
    total_drafted_articles: int
    avg_article_ratings: Decimal


# auth models
class TokenStatus(str, Enum):
    USED = "used"
    VALID = "valid"
    REVOKED = "revoked"


class RefreshTokenV1(BaseModel):
    token_id: UUID
    token: str
    user: AccountV1
    status: TokenStatus = TokenStatus.VALID
    created_at: datetime = datetime.now(timezone.utc)
    expires_at: datetime
    used_at: Optional[datetime] = None
    revoked_at: Optional[datetime] = None


# articles models
class ArticleStatusV1(str, Enum):
    PENDING = "pending"
    REVIEWING = "reviewing"
    EDITED = "edited"
    PUBLISHED = "published"


class ArticleCategoryV1(str, Enum):
    NEWS = "news"
    TRANSFERS = "transfers"


class ArticleStatV1(BaseModel):
    user: UserV1
    rating: Decimal = Field(decimal_places=1)
    is_rated: bool = False
    read_at: datetime = datetime.now(timezone.utc)


class ArticleImageV1(BaseModel):
    img_name: str
    img_type: str
    img_size: int


class ArticleV1(BaseModel):
    title: str = Field(min_length=15)
    content: str = Field(min_length=200)
    sport: SportV1
    author: AuthorV1
    editor: EditorV1 = None
    readers: list[ArticleStatV1] = []
    status: ArticleStatusV1 = ArticleStatusV1.PENDING
    images: list[ArticleImageV1] = []
    created_at: datetime = datetime.now(timezone.utc)


class ArticleDraftV1(BaseModel):
    draft_id: PydanticObjectId
    title: Optional[str] = Field(default=None, min_length=15)
    content: Optional[str] = Field(default=None, min_length=200)
    category: Optional[ArticleCategoryV1] = None
    sport: Optional[SportV1] = None
    author: Optional[AuthorV1] = None
    editor: Optional[EditorV1] = None
    athletes: Optional[list[str]] = None
    teams: Optional[list[str]] = None
    status: str = "draft"
    images: Optional[list[ArticleImageV1]] = None
    created_at: Optional[datetime] = None


class TeamSportV1(ArticleV1):
    category: Literal["news", "transfers"]
    teams: list[TeamV1]


class ArticleCreateV1(BaseModel):
    draft_id: Optional[PydanticObjectId] = Field(default=None)
    title: str = Field(min_length=15)
    content: str = Field(min_length=200)
    author: str
    sport: SportEnumv1
    category: ArticleCategoryV1 = ArticleCategoryV1.NEWS
    athletes: Optional[list[str]] = Field(default=None)
    teams: Optional[list[str]] = Field(default=None)
    images: Optional[list[str]] = None


class ArticleDraftCreateV1(BaseModel):
    title: Optional[str] = Field(default=None, min_length=15)
    content: Optional[str] = Field(default=None, min_length=200)
    author: Optional[str] = None
    sport: Optional[SportEnumv1] = None
    category: Optional[ArticleCategoryV1] = Field(default=ArticleCategoryV1.NEWS)
    athletes: Optional[list[str]] = Field(default=None)
    teams: Optional[list[str]] = Field(default=None)
    images: Optional[list[str]] = None


# tasks model
class TaskV1(BaseModel):
    assigned_by: AdminV1
    assigned_to: EditorV1
    article: ArticleV1
    type: str = "editing"
    created_at: datetime = datetime.now(timezone.utc)
