from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from tests.types import MainConfig


@pytest.fixture(scope="session", name="api_client")
def api_client(main_config: MainConfig) -> Generator[TestClient, None, None]:
    app = create_app(main_config)

    with TestClient(app, base_url="http://test", headers={"X-Request-Id": "123"}) as test_client:
        yield test_client
