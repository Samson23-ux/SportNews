import pymongo
from pymongo import IndexModel
from beanie import Document, Link
from typing import Optional, Literal
from datetime import datetime, timezone
from pydantic import Field, BaseModel, ConfigDict


from app.api.v1.schemas.users import UserV1
from app.api.v1.schemas.sports import TeamV1, SportV1


class ArticleV1(Document):
    title: str = Field(min_length=15)
    content: str = Field(min_length=200)
    author: Link[UserV1]
    created_at: datetime = datetime.now(timezone.utc)

    class Settings:
        # name of collections
        name: str = "articles"

        is_root: bool = True

        # list of indexes
        indexes: list = [
            IndexModel(
                [
                    ("title", pymongo.TEXT),
                    ("content", pymongo.TEXT)
                ],
                name="articles_index"
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
    title: str = Field(min_length=15)
    content: str = Field(min_length=200)
    author: str
    category: str = Field(default="news", description="Category of article. News or Transfers")
    athletes: list[str] = Field(description="A list of athletes the article is about")

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")


class ArticleUpdateV1(BaseModel):
    title: Optional[str] = Field(min_length=15)
    content: Optional[str] = Field(min_length=200)
    author: Optional[str]
    category: Optional[str] = Field(default=None, description="Category of article. News or Transfers")
    athletes: Optional[list[str]] = Field(default=None, description="A list of athletes the article is about")

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
            IndexModel(
                [("user", pymongo.ASCENDING)],
                name="subscriptions_user_index"
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


class SubscriptionCreateV1(BaseModel):
    sport_categories: list[str]
    is_active: bool

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")


class SubscriptionUpdateV1(BaseModel):
    sport_categories: Optional[list[str]] = None
    is_active: Optional[bool] = None

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
