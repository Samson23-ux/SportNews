from decimal import Decimal
from beanie import PydanticObjectId
from app.api.v1.schemas.tasks import TaskV1
from app.api.v1.schemas.auth import TokenStatus
from app.api.v1.schemas.sports import TeamV1, CompetitionV1, FootballV1
from app.api.v1.schemas.articles import (
    TeamSportV1,
    ArticleStatV1,
    ArticleDraftV1,
    ArticleImageV1,
    ArticleCreateV1,
    ArticleDraftCreateV1,
)
from app.api.v1.schemas.users import (
    UserV1,
    AdminV1,
    EditorV1,
    AuthorV1,
    EditorCreateV1,
    AuthorCreateV1,
    UserSettingsV1,
    WriterSettingsV1,
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

golf_competitions: list[CompetitionV1] = [golf_competition]
tennis_competitions: list[CompetitionV1] = [tennis_competition]
boxing_competitions: list[CompetitionV1] = [boxing_competition]

# football
football: FootballV1 = FootballV1(
    name="football", teams=football_teams, competitions=football_competitions
)


# article data
fake_article_content = """"""

article_img: ArticleImageV1 = ArticleImageV1(
    img_name="fake_image_url",
    img_type="jgp",
    img_size=222
)

article_title: str = "fake_title"
article_content: str = fake_article_content
article_sport: FootballV1 = football
article_category: str = "news"
article_author: AuthorV1 = fake_author
article_teams: list[TeamV1] = football_teams

fake_article: TeamSportV1 = TeamSportV1(
    title=article_title,
    content=article_content,
    author=article_author,
    sport=article_sport,
    category=article_category,
    teams=article_teams,
    images=[article_img]
)


# article with rating

user_data: dict = {
    "_id": PydanticObjectId("507f1f77bcf86cd799439011"),
    "email": user_email,
    "password": user_password,
    "profile_settings": user_settings
}

fake_user_1: UserV1 = UserV1.model_validate(user_data, extra="allow")

article_stat: ArticleStatV1 = ArticleStatV1(
    user=fake_user_1,
    rating=Decimal(6.6),
    is_rated=True
)

fake_article_with_rating: TeamSportV1 = TeamSportV1(
    title=article_title,
    content=article_content,
    author=article_author,
    sport=article_sport,
    category=article_category,
    teams=article_teams,
    readers=[article_stat]
)

# article draft
fake_draft: ArticleDraftV1 = ArticleDraftV1(
    draft_id=PydanticObjectId(),
    title=article_title,
    sport=article_sport,
)

# author and editor dashboard
fake_dashboard: dict = {
    "total_articles": 1,
    "total_article_readers": 1,
    "avg_article_readers": 1,
    "total_drafted_articles": 0,
    "avg_article_ratings": Decimal(8.0),
}

# admin dashboard
fake_dashboard_1: dict = {
    "total_articles": 1,
    "avg_article_readers": 1,
    "total_users": 1,
    "total_authors": 1,
    "total_editors": 1,
    "total_article_readers": {
        "total_readers": 1,
        "readers_who_rate": 0,
        "readers_who_dont_rate": 1
    }
}

# article create data
fake_article_create: ArticleCreateV1 = ArticleCreateV1(
    title=article_title,
    content=article_content,
    author="article_author",
    sport="football",
    category=article_category,
    teams=["fake_football_name"]
)

# draft create data
fake_draft_create: ArticleDraftCreateV1 = ArticleDraftCreateV1(
    title=article_title,
    content=article_content,
)

# task data
fake_task: TaskV1 = TaskV1(
    assigned_by=fake_admin,
    assigned_to=fake_editor,
    article=fake_article
)


# author and editor create data
fake_author_create: AuthorCreateV1 = AuthorCreateV1(
    name=author_name,
    nationality=author_nationality,
    user_id=PydanticObjectId()
)

fake_editor_create: EditorCreateV1 = EditorCreateV1(
    name=editor_name,
    nationality=editor_nationality,
    user_id=PydanticObjectId()
)
