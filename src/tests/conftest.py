import pytest

from app.api.dependencies.configs import get_main_config
from tests.types import MainConfig

pytest_plugins = ("tests.application.functional.plugins.api_client",)


@pytest.fixture(scope="session")
def main_config() -> MainConfig:
    return get_main_config()
