from app.api.v1.schemas.sports import TeamV1, CompetitionV1


fake_article_content = """"""

fake_user: dict = {
    "email": "fake_email@example.com",
    "password": "fake_password"
}

fake_admin: dict = {
    "name": "fake_editor_name",
    "nationality": "fake_nationality",
    "email": "fake_admin_email@example.com",
    "password": "fake_admin_password"
}

fake_author: dict = {
    "name": "fake_author_name",
    "nationality": "fake_nationality",
    "email": "fake_author_user_email@example.com",
    "password": "fake_author_user_password",
}

fake_editor: dict = {
    "name": "fake_editor_name",
    "nationality": "fake_nationality",
    "email": "fake_editor_user_email@example.com",
    "password": "fake_editor_user_password"
}

fake_article: dict = {
    "title": "fake_title",
    "content": fake_article_content,
    "author": fake_author.get("name"),
    "sport": "football",
    "category": "news",
    "athletes": ["fake_athlete"]
}

football_team: TeamV1 = TeamV1(name="fake_football_name", country="fake_country")
football_competition: CompetitionV1 = CompetitionV1(name="fake_football_competition", type="league")

basketball_team: TeamV1 = TeamV1(name="fake_basketball_name", country="fake_country")
basketball_competition: CompetitionV1 = CompetitionV1(name="fake_basketball_competition", type="league")

football_teams: list[TeamV1] = [football_team]
football_competitions: list[CompetitionV1] = [football_competition]

basketball_teams: list[TeamV1] = [basketball_team]
basketball_competitions: list[CompetitionV1] = [basketball_competition]

golf_competition: CompetitionV1 = CompetitionV1(name="fake_golf_competition", type="tournament")
tennis_competition: CompetitionV1 = CompetitionV1(name="fake_tennis_competition", type="tournament")
boxing_competition: CompetitionV1 = CompetitionV1(name="fake_boxing_competition", type="tournament")

golf_competitions: list[TeamV1] = [golf_competition]
tennis_competitions: list[CompetitionV1] = [tennis_competition]
boxing_competitions: list[CompetitionV1] = [boxing_competition]
