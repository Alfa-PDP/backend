import time
from typing import Generator

import pytest
from sqlalchemy import Engine, create_engine
from sqlalchemy_utils import create_database, drop_database

from tests.types import MainConfig


@pytest.fixture()
def single_use_database(main_config: MainConfig) -> Generator[Engine, None, None]:
    """
    SQLAlchemy engine, for single use
    """
    timestamp = str(int(time.time()))[-4:]
    db_url = f"{main_config.postgresql.database_url}{timestamp}"
    create_database(db_url)
    engine = create_engine(db_url, echo=True)
    try:
        yield engine
    finally:
        engine.dispose()
        drop_database(db_url)
