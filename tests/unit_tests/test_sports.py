import pytest
from unittest.mock import AsyncMock, patch
from pymongo.asynchronous.client_session import AsyncClientSession


from app.api.v1.schemas.users import UserV1
from tests.unit_tests.conftest import base_path
from app.core.exceptions import TeamsNotFoundError
from app.api.v1.services.sport_service import sport_service_v1
from tests.fake_data import fake_user, football, football_teams, football_competitions


@pytest.mark.asyncio
async def test_get_all_sports(verify_token: AsyncMock, get_session: AsyncClientSession):
    curr_user: UserV1 = fake_user
    refresh_token: str = "fake-refresh-token"

    path: str = f"{base_path}.sport_service.get_all_sports"
    with patch(path, new_callable=AsyncMock) as sports:
        sports.return_value = [football]
        sports_db = await sport_service_v1.get_all_sports(
            curr_user, get_session, refresh_token
        )

    assert sports_db
    verify_token.assert_awaited_once()
    sports.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_sport_teams(
    verify_token: AsyncMock, get_session: AsyncClientSession
):
    sport_name: str = "football"
    curr_user: UserV1 = fake_user
    refresh_token: str = "fake-refresh-token"

    path: str = f"{base_path}.sport_service.get_sport_teams"
    with patch(path, new_callable=AsyncMock) as teams:
        teams.return_value = football_teams
        teams_db = await sport_service_v1.get_sport_teams(
            sport_name, curr_user, refresh_token, get_session
        )

    assert teams_db
    verify_token.assert_awaited_once()
    teams.assert_awaited_once()


@pytest.mark.asyncio
async def test_sport_teams_not_found(
    verify_token: AsyncMock, get_session: AsyncClientSession
):
    sport_name: str = "football"
    curr_user: UserV1 = fake_user
    refresh_token: str = "fake-refresh-token"

    path: str = f"{base_path}.sport_service.get_sport_teams"
    teams_patch: AsyncMock = patch(path, new_callable=AsyncMock).start()

    teams_patch.return_value = None

    with pytest.raises(TeamsNotFoundError) as exc:
        await sport_service_v1.get_sport_teams(
            sport_name, curr_user, refresh_token, get_session
        )
    
    teams_patch.stop()

    "teams not found" == str(exc.value)
    verify_token.assert_awaited_once()
    teams_patch.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_sport_competitions(
    verify_token: AsyncMock, get_session: AsyncClientSession
):
    sport_name: str = "football"
    curr_user: UserV1 = fake_user
    refresh_token: str = "fake-refresh-token"

    path: str = f"{base_path}.sport_service.get_sport_competitions"
    with patch(path, new_callable=AsyncMock) as competitions:
        competitions.return_value = football_competitions
        teams_db = await sport_service_v1.get_sport_competitions(
            sport_name, curr_user, refresh_token, get_session
        )

    assert teams_db
    verify_token.assert_awaited_once()
    competitions.assert_awaited_once()
