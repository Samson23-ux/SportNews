from decimal import Decimal
from app.api.v1.schemas.auth import TokenStatus
from app.api.v1.schemas.articles import TeamSportV1
from app.api.v1.schemas.sports import TeamV1, CompetitionV1, FootballV1
from app.api.v1.schemas.users import (
    AdminV1,
    EditorV1,
    AuthorV1,
    UserV1,
    WriterSettingsV1,
    UserSettingsV1,
    EmployeeSettingsV1,
)

class FakeToken:
    def __init__(self, status: TokenStatus = TokenStatus.VALID):
        self.status = status

    @property
    def get_status(self):
        return self.status

# admin
admin_email: str = "fake_admin_email@example.com"
admin_password: str = "fake_admin_password"
admin_name: str = "fake_editor_name"
admin_nationality: str = "fake_nationality"
admin_settings: EmployeeSettingsV1 = EmployeeSettingsV1()

fake_admin: AdminV1 = AdminV1(
    email=admin_email,
    password=admin_password,
    name=admin_name,
    nationality=admin_nationality,
    profile_settings=admin_settings,
)

# editor
editor_name: str = "fake_editor_name"
editor_email: str = "fake_editor_user_email@example.com"
editor_password: str = "fake_editor_user_password"
editor_nationality: str = "fake_nationality"
editor_settings: WriterSettingsV1 = WriterSettingsV1()

fake_editor: EditorV1 = EditorV1(
    email=editor_email,
    password=editor_password,
    name=editor_name,
    nationality=editor_nationality,
    profile_settings=editor_settings,
)

# author
author_name: str = "fake_author_name"
author_email: str = "fake_author_user_email@example.com"
author_password: str = "fake_author_user_password"
author_nationality: str = "fake_nationality"
author_settings: WriterSettingsV1 = WriterSettingsV1()

fake_author: AuthorV1 = AuthorV1(
    email=author_email,
    password=author_password,
    name=author_name,
    nationality=author_nationality,
    profile_settings=author_settings,
)

# user
user_email: str = "fake_email@example.com"
user_password: str = "fake_password"
user_settings: UserSettingsV1 = UserSettingsV1()

fake_user: UserV1 = UserV1(
    email=user_email, password=user_password, profile_settings=user_settings
)


# sport teams and competitions
football_team: TeamV1 = TeamV1(name="fake_football_name", country="fake_country")
football_competition: CompetitionV1 = CompetitionV1(
    name="fake_football_competition", type="league"
)

basketball_team: TeamV1 = TeamV1(name="fake_basketball_name", country="fake_country")
basketball_competition: CompetitionV1 = CompetitionV1(
    name="fake_basketball_competition", type="league"
)

football_teams: list[TeamV1] = [football_team]
football_competitions: list[CompetitionV1] = [football_competition]

basketball_teams: list[TeamV1] = [basketball_team]
basketball_competitions: list[CompetitionV1] = [basketball_competition]

golf_competition: CompetitionV1 = CompetitionV1(
    name="fake_golf_competition", type="tournament"
)
tennis_competition: CompetitionV1 = CompetitionV1(
    name="fake_tennis_competition", type="tournament"
)
boxing_competition: CompetitionV1 = CompetitionV1(
    name="fake_boxing_competition", type="tournament"
)

golf_competitions: list[TeamV1] = [golf_competition]
tennis_competitions: list[CompetitionV1] = [tennis_competition]
boxing_competitions: list[CompetitionV1] = [boxing_competition]

# football
football: FootballV1 = FootballV1(
    name="football", teams=football_teams, competitions=football_competitions
)

# article data
fake_article_content = """"""

article_title: str = "fake_title"
article_content: str = fake_article_content
article_sport: FootballV1 = football
article_category: str = "news"
article_author: AuthorV1 = fake_author
article_teams: list[TeamV1] = football_teams

fake_article: TeamSportV1 = TeamSportV1(
    title=article_title,
    content=article_content,
    sport=article_sport,
    category=article_category,
    author=article_author,
    teams=article_teams
)

# author and editor dashboard
fake_dashboard: dict = {
    "total_articles": 1,
    "total_article_readers": 1,
    "avg_article_readers": 1,
    "total_drafted_articles": 0,
    "avg_article_ratings": Decimal(8.0)
}

