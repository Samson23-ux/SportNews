import pymongo
from pymongo import IndexModel
from pydantic import BaseModel
from datetime import datetime, timezone
from beanie import Document, Link, PydanticObjectId


from app.api.v1.schemas.users import EditorV1, AdminV1
from app.api.v1.schemas.articles import ArticleV1


class TaskV1(Document):
    assigned_by: Link[AdminV1]
    assigned_to: Link[EditorV1]
    article: Link[ArticleV1]
    type: str = "editing"
    created_at: datetime = datetime.now(timezone.utc)

    class Settings:
        name = "tasks"

        # list of indexes
        indexes: list = [
            IndexModel(
                [("assigned_by", pymongo.ASCENDING)],
                name="tasks_assigned_by_index"
            ),
            IndexModel(
                [("assigned_to", pymongo.ASCENDING)],
                name="tasks_assigned_to_index"
            ),
            IndexModel(
                [("article", pymongo.ASCENDING)],
                name="tasks_article_index"
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


class BaseResponsev1(BaseModel):
    message: str


class TaskOutV1(BaseModel):
    id: PydanticObjectId
    assigned_by: str
    assigned_to: str
    article: ArticleV1
    type: str = "editing"
    created_at: datetime = datetime.now(timezone.utc)


class TaskresponseV1(BaseResponsev1):
    data: TaskOutV1 | list[TaskOutV1]
