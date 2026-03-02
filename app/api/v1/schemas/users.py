import pymongo
from enum import Enum
from decimal import Decimal
from typing import Optional
from pymongo import IndexModel
from datetime import datetime, timezone
from beanie import Document, PydanticObjectId
from pydantic import Field, EmailStr, field_validator, BaseModel, ConfigDict


from app.api.v1.schemas.sports import TeamV1


class UserRoleV1(str, Enum):
    USER: str = "user"
    ADMIN: str = "admin"
    AUTHOR: str = "author"
    EDITOR: str = "editor"


class Theme(str, Enum):
    DARK: str = "dark"
    WHITE: str = "white"


class UserCreateV1(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")


    @field_validator("email", mode="after")
    @classmethod
    def email_to_lower(cls, v: EmailStr):
        return v.lower()
    

class EmployeeCreateV1(UserCreateV1):
    name: str
    nationality: str


class AdminCreateV1(EmployeeCreateV1):
    pass


class EditorCreateV1(EmployeeCreateV1):
    pass


class AuthorCreateV1(EmployeeCreateV1):
    pass


class EmployeeUpdateV1(BaseModel):
    name: Optional[str] = None
    nationality: Optional[str] = None

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")


class AdminUpdateV1(EmployeeUpdateV1):
    pass


class EditorUpdateV1(EmployeeUpdateV1):
    pass


class AuthorUpdateV1(EmployeeUpdateV1):
    pass


class PasswordUpdateV1(BaseModel):
    curr_password: str
    new_password: str = Field(min_length=8)

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")


# global profile settings
class ProfileSettingsV1(BaseModel):
    timezone: str
    theme: Theme = Theme.WHITE


class UserSettingsV1(ProfileSettingsV1):
    receive_infomation: bool = False
    receive_newsletter: bool = False


class EmployeeSettingsV1(ProfileSettingsV1):
    pass


# settings class for authors and editors
class WriterSettingsV1(EmployeeSettingsV1):
    auto_delete_drafts: bool = False


class SettingsUpdateV1(BaseModel):
    timezone: Optional[str] = None
    theme: Optional[Theme] = None

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")


class UserSettingsUpdateV1(SettingsUpdateV1):
    receive_infomation: Optional[bool] = None
    receive_newsletter: Optional[bool] = None


class EmployeeSettingsUpdateV1(SettingsUpdateV1):
    pass


class WriterSettingsUpdateV1(EmployeeSettingsUpdateV1):
    auto_delete_drafts: Optional[bool] = None


# db data
class AccountV1(Document):
    email: EmailStr
    password: str = Field(min_length=8)
    is_verified: bool
    created_at: datetime = datetime.now(timezone.utc)

    class Settings:
        # name of collections
        name: str = "users"

        is_root: bool = True

        # list of indexes
        indexes: list = [
            IndexModel(
                [("email", pymongo.ASCENDING)],
                unique=True,
                name="users_email_index"
            )
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

        """
        for nested objects
        when set to true, the whole object is replaced with
        the update and not just the changed attribute
        e.g a = Example(attributes: {att1: 1.0, att2: 2.0})
        a.attributes = {att1: 3.0}
        a.save_changes()
        the attributes field now becomes {att1: 1.0} when set to true
        and not {att1: 3.0, att2: 2.0}
        to update just att1, the field value is changed instead
        a.attributes.att1 = 3.0
        """
        state_management_replace_objects: bool = True


class EmployeeV1(AccountV1):
    name: str
    nationality: str
    profile_settings: EmployeeSettingsV1

    class Settings:
        indexes: list = [
            IndexModel(
                [("name", pymongo.ASCENDING)],
                unique=True,
                name="superuser_name_index"
            )
        ]


class AdminV1(EmployeeV1):
    role: UserRoleV1 = UserRoleV1.ADMIN


class EditorV1(EmployeeV1):
    role: UserRoleV1 = UserRoleV1.EDITOR
    tasks: int
    profile_settings: WriterSettingsV1


class AuthorV1(EmployeeV1):
    role: UserRoleV1 = UserRoleV1.AUTHOR
    profile_settings: WriterSettingsV1


class UserV1(AccountV1):
    role: UserRoleV1 = UserRoleV1.USER
    favourite_teams: list[TeamV1]
    profile_settings: UserSettingsV1


# return data
class BaseResponseV1(BaseModel):
    message: str


class UserOutV1(BaseModel):
    id: PydanticObjectId
    email: EmailStr
    is_verified: bool
    role: UserRoleV1 = UserRoleV1.USER
    favourite_teams: list[TeamV1]
    profile_settings: UserSettingsV1
    created_at: datetime


class EmployeeOutV1(UserOutV1):
    name: str
    nationality: str
    profile_settings: EmployeeSettingsV1


class WriterOutV1(EmployeeOutV1):
    avg_article_ratings: Decimal
    profile_settings: WriterSettingsV1


class EmployeeDashboardV1(BaseModel):
    total_articles: int
    total_article_readers: int
    avg_article_readers: int


class AdminDashboardV1(EmployeeDashboardV1):
    total_users: int
    total_authors: int
    total_editors: int
    readers_who_rate: int
    total_article_readers: dict[str, int]


class WriterDashboardV1(EmployeeDashboardV1):
    total_published_articles: int
    total_drafted_articles: int
    avg_article_ratings: Decimal


class UserSettingsOutV1(BaseModel):
    settings: UserSettingsV1


class EmployeeSettingsOutV1(BaseModel):
    settings: EmployeeSettingsV1


class WriterSettingsOutV1(BaseModel):
    settings: EmployeeSettingsV1


# responses
class UserResponseV1(BaseResponseV1):
    data: Optional[UserOutV1 | list[UserOutV1]] = None


class AdminResponseV1(BaseResponseV1):
    data: Optional[EmployeeOutV1 | list[EmployeeOutV1]] = None


class WriterResponseV1(BaseResponseV1):
    data: Optional[WriterOutV1 | list[WriterOutV1]] = None


class SettingsResponseV1(BaseResponseV1):
    data: WriterSettingsOutV1 | UserSettingsOutV1 | EmployeeSettingsV1


class DashboardResponseV1(BaseResponseV1):
    data: AdminDashboardV1 | WriterDashboardV1
