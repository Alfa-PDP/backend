from http import HTTPStatus
from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select

from app.schemas.goals import CreateGoal
from app.schemas.users import CreateUserSchema
from database.models.goal import Goal
from database.models.team import Team
from database.models.user import User
from database.models.user_team import UserTeam


@pytest.mark.parametrize(
    ("method", "route", "params", "json", "expected_status"),
    [
        ("GET", "/api/v1/status", None, None, HTTPStatus.OK),
    ],
)
def test_http_ok(api_client: TestClient, method: str, route: str, params: Any, json: Any, expected_status: int) -> None:
    """
    Минимальный тест который помогает проверить что приложение не падает при попытке обратиться на эндпоинт,
    легко добавить еще один параметр даже до того его писать чтобы было удобно проверять.
    Большие запросы лучше убрать в переменные где-нибудь над тестом для читаемости
    """
    response = api_client.request(method=method, url=route, json=json, params=params)
    assert response.status_code == expected_status


def test_read_main(api_client: TestClient):
    response = api_client.request(method="GET", url="/api/v1/status/", json=None, params=None)
    assert response.status_code == 200


@pytest.fixture()
async def test_user_with_goals(db_session, api_client: TestClient):
    user_data = CreateUserSchema(
        name="John",
        family_name="Family",
        middle_name="Middle",
        position="SEO",
        avatar="https://cdn0.iconfinder.com/data/icons/user-pictures/100/malecostume-512.png"
    )

    # response = api_client.post("/api/v1/users", json=user_data.model_dump())
    # assert response.status_code == HTTPStatus.CREATED
    #
    # assert response.headers['Content-Type'] == 'application/json'
    #
    # async with db_session as session:
    #     user_repository = SQLAlchemyUserRepository(session)
    #     first_user_from_db = await user_repository.get_first_user()
    #
    #     assert first_user_from_db is not None
    #     assert first_user_from_db.name == user_data.name
    #     assert first_user_from_db.family_name == user_data.family_name
    #     assert first_user_from_db.middle_name == user_data.middle_name
    #     assert first_user_from_db.position == user_data.position
    #     assert first_user_from_db.avatar == user_data.avatar
    #
    #     # Создание команды
    #     team = Team(team_name="Random", leader_id=first_user_from_db.id)
    #     session.add(team)
    #     await session.flush()  # Используйте flush(), чтобы получить сгенерированный id
    #     team_id = team.id  # Получите сгенерированный id
    #     await session.commit()
    #
    #     # Создание связи
    #     user_team_relation = UserTeam(user_id=first_user_from_db.id, team_id=team_id)
    #     session.add(user_team_relation)
    #     await session.commit()
    async with db_session as session:
        user = User(**user_data.model_dump())
        session.add(user)
        await session.commit()

        # Создаем команду и устанавливаем связь с пользователем
        team = Team(team_name="Random", leader_id=user.id)
        session.add(team)
        await session.commit()

        # Устанавливаем связь между пользователем и командой
        user_team_relation = UserTeam(user_id=user.id, team_id=team.id)
        session.add(user_team_relation)
        await session.commit()

        assert user is not None
        assert user.name == user_data.name
        assert user.family_name == user_data.family_name
        assert user.middle_name == user_data.middle_name
        assert user.position == user_data.position
        assert user.avatar == user_data.avatar

    return user

@pytest.mark.parametrize(
    ("method", "route", "params", "json", "expected_status"),
    [
        ("GET", "/api/v1/users", None, None, HTTPStatus.NOT_FOUND),
        ("GET", "/api/v1/users/me", None, None, HTTPStatus.NOT_FOUND),
    ],
)
def test_users_endpoints(api_client: TestClient, method: str, route: str, params: Any, json: Any,
                         expected_status: int) -> None:
    response = api_client.request(method=method, url=route, json=json, params=params)
    assert response.status_code == expected_status


# @pytest.mark.asyncio
# async def test_get_user_tasks(db_session, api_client: TestClient, test_user_with_goals) -> None:
#     user_id = str((await test_user_with_goals).id)
#     response = api_client.get(f"/api/v1/users/{str(user_id)}/tasks", params={"year": "2022"})
#     assert response.status_code == HTTPStatus.NOT_FOUND
#     assert response.json() == {'detail': 'Not Found'}


@pytest.mark.asyncio
async def test_get_goals_for_user(db_session, api_client: TestClient, test_user_with_goals) -> None:
    user_id = str((await test_user_with_goals).id)
    response = api_client.get(f"/api/v1/users/{user_id}/goals")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Not Found'}


@pytest.mark.asyncio
async def test_create_goal(api_client: TestClient, db_session, test_user_with_goals) -> None:
    user = str((await test_user_with_goals).id)
    goal_data = CreateGoal(
        user_id=user,
        goal_name="Test Goal Name",
        employee_side_plus="Test Employee Side Plus",
        employee_side_minus="Test Employee Side Minuses",
    )
    data_dict = goal_data.model_dump()
    data_dict['user_id'] = str(data_dict['user_id'])

    response = api_client.post(f"/api/v1/goals", json=data_dict)
    assert response.status_code == HTTPStatus.CREATED

    async with db_session as session:
        # goal_repository = SqlAlchemyGoalRepository(session)
        query = select(Goal).where(Goal.user_id == user)
        result = await session.execute(query)
        goal = result.scalars().first()
        # goal = await goal_repository.get_by_user_id_or_none(user_id=(await test_user_with_goals).id)

        assert goal is not None
        assert goal.user_id == goal_data.user_id
        assert goal.goal_name == goal_data.goal_name
        assert goal.employee_side_plus == goal_data.employee_side_plus
        assert goal.employee_side_minus == goal_data.employee_side_minus
