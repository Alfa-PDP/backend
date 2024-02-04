from http import HTTPStatus
from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.repositories.users import SQLAlchemyUserRepository
from app.schemas.users import CreateUserSchema


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


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("name", "family_name", "middle_name", "position", "avatar", "expected_status"),
    [
        ("John", "Family", "Middle", "SEO",
         "https://cdn0.iconfinder.com/data/icons/user-pictures/100/malecostume-512.png", HTTPStatus.CREATED),
    ],
)
async def test_create_user_and_get_id(create_session, api_client: TestClient, name: str,
                                      family_name: str, middle_name: str, position: str, avatar: str,
                                      expected_status: int) -> None:
    user_data = CreateUserSchema(name=name, family_name=family_name, middle_name=middle_name, position=position,
                                 avatar=avatar)
    response = api_client.post("/api/v1/users", json=user_data.model_dump())

    assert response.status_code == expected_status

    assert response.headers['Content-Type'] == 'application/json'

    async with create_session() as session:
        user_repository = SQLAlchemyUserRepository(session)
        first_user_from_db = await user_repository.get_first_user()

        assert first_user_from_db is not None
        assert first_user_from_db.name == name
        assert first_user_from_db.family_name == family_name
        assert first_user_from_db.middle_name == middle_name
        assert first_user_from_db.position == position
        assert first_user_from_db.avatar == avatar
