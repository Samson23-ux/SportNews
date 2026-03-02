import pymongo
from uuid import UUID
from enum import Enum
from typing import Optional
from pymongo import IndexModel
from beanie import Document, Link
from datetime import datetime, timezone
from pydantic import EmailStr, BaseModel


from app.api.v1.schemas.users import AccountV1


class TokenStatus(str, Enum):
    USED: str = "used"
    VALID: str = "valid"
    REVOKED: str = "revoked"


class CodeStatus(str, Enum):
    USED: str = "used"
    VALID: str = "valid"


class TokenDataV1(BaseModel):
    email: EmailStr


class TokenV1(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RefreshTokenV1(Document):
    token_id: UUID
    token: str
    user: Link[AccountV1]
    status: TokenStatus = TokenStatus.VALID
    created_at: datetime = datetime.now(timezone.utc)
    expires_at: datetime
    used_at: Optional[datetime] = None
    revoked_at: Optional[datetime] = None

    class Settings:
        # name of collections
        name: str = "refresh_tokens"

        # list of indexes
        indexes: list = [
            IndexModel(
                [("token_id", pymongo.ASCENDING)],
                unique=True,
                name="refresh_tokens_token_id_index"
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


class EmailCodeV1(Document):
    user: Link[AccountV1]
    code: str
    mode: str
    status: CodeStatus = CodeStatus.VALID
    created_at: datetime = datetime.now(timezone.utc)

    class Settings:
        # name of collections
        name: str = "email_codes"

        # list of indexes
        indexes: list = [
            IndexModel(
                [("code", pymongo.ASCENDING)],
                name="email_codes_code_index"
            ),
            IndexModel(
                [("created_at", pymongo.ASCENDING)],
                expireAfterSeconds=300,
                name="email_codes_created_at_index"
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
