import pymongo
from enum import Enum
from beanie import Document
from pymongo import IndexModel
from pydantic import BaseModel


class CompetitionTypeV1(str, Enum):
    LEAGUE: str = "league"
    EUROPE: str = "europe"
    TOURNAMENT: str = "tournament"
    CHAMPIONSHIP: str = "championship"


class SportEnumv1(str, Enum):
    FOOTBALL: str = "football"
    BASKETBALL: str = "basketball"
    TENNIS: str = "tennis"
    GOLF: str = "golf"
    BOXING: str = "boxing"


class SportV1(Document):
    name: str


    class Settings:
        # name of collections
        name: str = "sports"

        is_root: bool = True

        # list of indexes
        indexes: list = [
            IndexModel(
                [("name", pymongo.ASCENDING)],
                unique=True,
                name="sports_name_index"
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


class TeamV1(BaseModel):
    name: str
    country: str

class CompetitionV1(BaseModel):
    name: str
    type: CompetitionTypeV1


class FootballV1(SportV1):
    teams: list[TeamV1]
    competitions: list[CompetitionV1]


class BasketballV1(SportV1):
    teams: list[TeamV1]
    competitions: list[CompetitionV1]


class TennisV1(SportV1):
    competitions: list[CompetitionV1]


class BoxingV1(SportV1):
    competitions: list[CompetitionV1]


class GolfV1(SportV1):
    competitions: list[CompetitionV1]
