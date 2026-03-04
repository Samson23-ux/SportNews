import pymongo
from enum import Enum
from decimal import Decimal
from pymongo import IndexModel
from typing import Optional, Literal
from datetime import datetime, timezone
from pydantic import Field, BaseModel, ConfigDict
from beanie import Document, Link, PydanticObjectId


from app.api.v1.schemas.users import UserV1, AuthorV1, EditorV1
from app.api.v1.schemas.sports import TeamV1, SportV1, SportEnumv1


class ArticleCategoryV1(str, Enum):
    NEWS: str = "news"
    TRANSFERS: str = "transfers"


class ArticleStatusV1(str, Enum):
    PENDING: str = "pending"
    REVIEWING: str = "reviewing"
    EDITED: str = "edited"
    PUBLISHED: str = "published"


class ArticleStatV1(BaseModel):
    user: UserV1
    rating: Decimal = Field(decimal_places=1)
    is_rated: bool = False
    read_at: datetime = datetime.now(timezone.utc)


class ArticleImageV1(BaseModel):
    img_name: str
    img_type: str
    img_size: str


class ArticleV1(Document):
    title: str = Field(min_length=15)
    content: str = Field(min_length=200)
    sport: Link[SportV1]
    author: Link[AuthorV1]
    editor: Link[EditorV1] = None
    readers: list[ArticleStatV1] = []
    status: ArticleStatusV1 = ArticleStatusV1.PENDING
    images: list[ArticleImageV1] = []
    created_at: datetime = datetime.now(timezone.utc)

    class Settings:
        # name of collections
        name: str = "articles"

        is_root: bool = True

        # list of indexes
        indexes: list = [
            IndexModel(
                [("title", pymongo.TEXT), ("content", pymongo.TEXT)],
                name="articles_index",
            ),
        ]

        """
        revision id ensures the local data is in sync with
        the data in db before allowing changes to be made
        this ensures data consistency and prevents data loss
        """
        use_revision: bool = True

        """
        allow beanie track current changes not saved to db yet
        """
        use_state_management: bool = True

        """
        allow beanie track previous changes saved to db
        """
        state_management_save_previous: bool = True

        state_management_replace_objects: bool = True


class ArticleDraftV1(Document):
    draft_id: PydanticObjectId
    title: Optional[str] = Field(default=None, min_length=15)
    content: Optional[str] = Field(default=None, min_length=200)
    category: Optional[ArticleCategoryV1] = None
    sport: Optional[Link[SportV1]] = None
    author: Optional[Link[AuthorV1]] = None
    editor: Optional[Link[EditorV1]] = None
    athletes: Optional[list[str]] = None
    teams: Optional[list[str]] = None
    status: str = "draft"
    images: Optional[list[ArticleImageV1]] = None
    created_at: Optional[datetime] = None

    class Settings:
        # name of collections
        name: str = "article_drafts"

        # list of indexes
        indexes: list = [
            IndexModel(
                [("draft_id", pymongo.ASCENDING)],
                name="article_drafts_draft_id",
            ),
        ]

        """
        revision id ensures the local data is in sync with
        the data in db before allowing changes to be made
        this ensures data consistency and prevents data loss
        """
        use_revision: bool = True

        """
        allow beanie track current changes not saved to db yet
        """
        use_state_management: bool = True

        """
        allow beanie track previous changes saved to db
        """
        state_management_save_previous: bool = True


# article for team sport
class TeamSportV1(ArticleV1):
    category: Literal["news", "transfers"]
    teams: list[TeamV1]


# article for individual sport
class IndividualSportV1(ArticleV1):
    category: Literal["news"]
    athletes: list[str]


class ArticleCreateV1(BaseModel):
    draft_id: Optional[PydanticObjectId] = Field(
        default=None,
        description="Provide a draft id if an article from a draft is to be posted",
    )
    title: str = Field(min_length=15)
    content: str = Field(min_length=200)
    author: str
    sport: SportEnumv1
    category: ArticleCategoryV1 = ArticleCategoryV1.NEWS
    athletes: Optional[list[str]] = Field(
        default=None,
        description="A list of athletes (for individual sport) the article is about",
    )
    teams: Optional[list[str]] = Field(
        default=None,
        description="A list of teams (for team sport) the article is about",
    )
    images: Optional[list[str]] = None

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")


class ArticleUpdateV1(BaseModel):
    title: Optional[str] = Field(default=None, min_length=15)
    content: Optional[str] = Field(default=None, min_length=200)
    author: Optional[str] = None
    sport: Optional[SportEnumv1] = None
    category: Optional[ArticleCategoryV1] = Field(
        default=ArticleCategoryV1.NEWS,
        description="Category of article. News or Transfers",
    )
    athletes: Optional[list[str]] = Field(
        default=None,
        description="A list of athletes (for individual sport) the article is about",
    )
    teams: Optional[list[str]] = Field(
        default=None,
        description="A list of teams (for teams sport) the article is about",
    )
    images: Optional[list[str]] = None

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")


class ArticleDraftCreateV1(BaseModel):
    title: Optional[str] = Field(default=None, min_length=15)
    content: Optional[str] = Field(default=None, min_length=200)
    author: Optional[str] = None
    sport: Optional[SportEnumv1] = None
    category: Optional[ArticleCategoryV1] = Field(
        default=ArticleCategoryV1.NEWS,
        description="Category of article. News or Transfers",
    )
    athletes: Optional[list[str]] = Field(
        default=None,
        description="A list of athletes (for individual sport) the article is about",
    )
    teams: Optional[list[str]] = Field(
        default=None,
        description="A list of teams (for teams sport) the article is about",
    )
    images: Optional[list[str]] = None

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")


# Subscription
"""to receive articles in email when published"""


class SubscriptionV1(Document):
    user: Link[UserV1]
    sport_categories: list[Link[SportV1]]
    is_active: bool
    created_at: datetime = datetime.now(timezone.utc)

    class Settings:
        # name of collections
        name: str = "subscriptions"

        # list of indexes
        indexes: list = [
            IndexModel([("user", pymongo.ASCENDING)], name="subscriptions_user_index"),
        ]

        """
        revision id ensures the local data is in sync with
        the data in db before allowing changes to be made
        this ensures data consistency and prevents data loss
        """
        use_revision: bool = True

        """
        allow beanie track current changes not saved to db yet
        """
        use_state_management: bool = True

        """
        allow beanie track previous changes saved to db
        """
        state_management_save_previous: bool = True


class SubscriptionCreateV1(BaseModel):
    sport_categories: list[str]
    is_active: bool

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")


class SubscriptionUpdateV1(BaseModel):
    sport_categories: Optional[list[str]] = None
    is_active: Optional[bool] = None

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")


# return data
class BaseResponseV1(BaseModel):
    message: str


class ArticleOutV1(BaseModel):
    id: PydanticObjectId
    title: str
    content: str
    sport: str
    author: str
    editor: Optional[str] = None
    athletes: Optional[list[str]] = None
    avg_rating: Decimal
    category: ArticleCategoryV1
    created_at: datetime


class ArticleDraftOutV1(BaseModel):
    id: PydanticObjectId
    draft_id: PydanticObjectId
    title: Optional[str] = None
    content: Optional[str] = None
    sport: Optional[str] = None
    author: Optional[str] = None
    editor: Optional[str] = None
    athletes: Optional[list[str]] = None
    category: Optional[ArticleCategoryV1] = None
    created_at: datetime


class ArticleReadersV1(BaseModel):
    readers: int


class ImageOutV1(ArticleImageV1):
    pass


class ArticleResponseV1(BaseResponseV1):
    data: ArticleOutV1 | list[ArticleOutV1] | ArticleReadersV1


class ArticleDraftResponseV1(BaseResponseV1):
    data: ArticleDraftOutV1 | list[ArticleDraftOutV1]


class ImageResponseV1(BaseResponseV1):
    data: list[ImageOutV1]
