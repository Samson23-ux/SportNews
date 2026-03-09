from app.api.v1.schemas.sports import (
    FootballV1,
    BasketballV1,
    TennisV1,
    BoxingV1,
    GolfV1,
    TeamV1,
    CompetitionV1,
)


class SportCategory:
    def __init__(self, name: str):
        self.name = name

    async def add_football(
        self, teams: list[TeamV1], competitions: list[CompetitionV1]
    ):
        pass

    async def add_basketball(
        self, teams: list[TeamV1], competitions: list[CompetitionV1]
    ):
        pass

    async def add_tennis(self, competitions: list[CompetitionV1]):
        pass

    async def add_golf(self, competitions: list[CompetitionV1]):
        pass

    async def add_boxing(self, competitions: list[CompetitionV1]):
        pass
