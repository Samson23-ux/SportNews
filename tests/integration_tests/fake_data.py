from uuid import uuid4
from decimal import Decimal
from beanie import PydanticObjectId
from app.api.v1.schemas.tasks import TaskV1
from datetime import datetime, timedelta, timezone
from app.api.v1.schemas.auth import RefreshTokenV1
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
    AdminDashboardV1,
    WriterDashboardV1,
    EmployeeSettingsV1,
)


# article data
fake_article_content = """
The Role of Sports in Personal Development and Society
Sports have long played an important role in human culture, serving as a source of
entertainment, competition, and personal development. Across the world, millions of people
participate in sports either professionally or recreationally. From football and basketball
to tennis and athletics, sports bring people together, promote healthy lifestyles, and help
individuals develop valuable life skills.
One of the most significant benefits of sports is the improvement of physical health. Regular
participation in sports helps individuals maintain a healthy body by strengthening muscles,
improving cardiovascular fitness, and increasing overall endurance. Activities such as running,
swimming, and cycling not only help control weight but also reduce the risk of diseases such as
obesity, heart disease, and diabetes. In addition, sports encourage people to remain active
rather than adopting sedentary lifestyles.
Beyond physical health, sports contribute greatly to mental well-being. Engaging in physical
activity releases endorphins, which are chemicals in the brain that help reduce stress and
improve mood. Many athletes report feeling more confident and focused as a result of their
involvement in sports. For students and young people in particular, sports can provide a healthy
outlet for stress and a way to maintain a balanced lifestyle alongside academic responsibilities.
Sports also play a vital role in teaching important life skills. Team sports such as football,
basketball, and volleyball require cooperation, communication, and trust among teammates.
Players learn the value of teamwork and understand that success often depends on collective
effort rather than individual performance. Additionally, sports teach discipline, time management,
and perseverance. Athletes must train regularly, follow rules, and continue improving even after
experiencing losses or setbacks.
Another powerful aspect of sports is their ability to unite communities and nations. Major
sporting events such as the Olympics and international tournaments bring people from different
backgrounds together to celebrate competition and achievement. Fans support their teams with
passion, creating a sense of identity and belonging. Sports can bridge cultural differences and
foster mutual respect among individuals who might otherwise have little interaction.
In conclusion, sports offer far more than just entertainment. They promote physical and mental
health, teach valuable life lessons, and strengthen communities. Whether played professionally
or simply for fun, sports remain an essential part of human society and continue to inspire
people around the world to stay active, disciplined, and connected.
"""


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


# auth token
fake_token: RefreshTokenV1 = RefreshTokenV1(
    token_id=uuid4(),
    token="fake-auth-token",
    user=fake_user,
    expires_at=datetime.now(tz=timezone.utc) + timedelta(days=7),   
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

article_img: ArticleImageV1 = ArticleImageV1(
    img_name="fake_image_url", img_type="jgp", img_size=222
)

article_title: str = "fake article title about football"
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
    images=[article_img],
)


# article with rating
fake_user_1: UserV1 = UserV1(
    id=PydanticObjectId("507f1f77bcf86cd799439011"),
    email=user_email,
    password=user_password,
    profile_settings=user_settings
)

article_stat: ArticleStatV1 = ArticleStatV1(
    user=fake_user_1, rating=Decimal("6.6"), is_rated=True
)

fake_article_with_rating: TeamSportV1 = TeamSportV1(
    title=article_title,
    content=article_content,
    author=article_author,
    sport=article_sport,
    category=article_category,
    teams=article_teams,
    readers=[article_stat],
)

# article draft
fake_draft: ArticleDraftV1 = ArticleDraftV1(
    draft_id=PydanticObjectId(),
    title=article_title,
    sport=article_sport,
)

# author and editor dashboard
fake_dashboard: WriterDashboardV1 = WriterDashboardV1(
    total_articles=1,
    total_article_readers=1,
    avg_article_readers=1,
    total_drafted_articles=0,
    total_published_articles=1,
    avg_article_ratings=Decimal("8.0"),
)

# admin dashboard
fake_dashboard_1: AdminDashboardV1 = AdminDashboardV1(
    total_articles=1,
    avg_article_readers=1,
    total_users=1,
    total_authors=1,
    total_editors=1,
    total_article_readers={
        "total_readers": 1,
        "readers_who_rate": 0,
        "readers_who_dont_rate": 1,
    },
)


# article create data
fake_article_create: ArticleCreateV1 = ArticleCreateV1(
    title=article_title,
    content=article_content,
    author="article_author",
    sport="football",
    category=article_category,
    teams=["fake_football_name"],
)

# draft create data
fake_draft_create: ArticleDraftCreateV1 = ArticleDraftCreateV1(
    title=article_title,
    content=article_content,
)

# task data
fake_task: TaskV1 = TaskV1(
    assigned_by=fake_admin, assigned_to=fake_editor, article=fake_article
)


# author and editor create data
fake_author_create: AuthorCreateV1 = AuthorCreateV1(
    name=author_name, nationality=author_nationality, user_id=PydanticObjectId()
)

fake_editor_create: EditorCreateV1 = EditorCreateV1(
    name=editor_name, nationality=editor_nationality, user_id=PydanticObjectId()
)
