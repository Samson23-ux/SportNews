import pymongo
from enum import Enum
from beanie import Document
from pymongo import IndexModel
from datetime import datetime, timezone
from pydantic import Field, EmailStr, field_validator, BaseModel, ConfigDict


from app.api.v1.schemas.sports import TeamV1


class UserRoleV1(str, Enum):
    USER: str = "user"
    ADMIN: str = "admin"
    AUTHOR: str = "author"


class Theme(str, Enum):
    DARK: str = "dark"
    WHITE: str = "white"


class TimeZone(str, Enum):
    pass


class UserCreateV1(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")


    @field_validator("email", mode="after")
    @classmethod
    def email_to_lower(cls, v: EmailStr):
        return v.lower()


class PasswordUpdateV1(BaseModel):
    curr_password: str
    new_password: str = Field(min_length=8)

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")


class ProfileSetting(BaseModel):
    theme: Theme = Theme.WHITE.value
    receive_info: bool = False
    receive_newsletter: bool = False
    timezone: TimeZone


class UserV1(Document):
    email: EmailStr
    password: str = Field(min_length=8)
    is_verified: bool
    roles: list[UserRoleV1] = [UserRoleV1.USER.value]
    favourite_teams: list[TeamV1]
    profile_settings: ProfileSetting
    created_at: datetime = datetime.now(timezone.utc)

    class Settings:
        # name of collections
        name: str = "users"

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
