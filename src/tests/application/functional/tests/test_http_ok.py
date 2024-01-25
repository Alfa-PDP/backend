from http import HTTPStatus
from typing import Any

import pytest
from fastapi.testclient import TestClient


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
