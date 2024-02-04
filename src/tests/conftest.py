from typing import AsyncGenerator, Any

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

from app.api.dependencies.configs import get_main_config
from database.models.declarative_base import BaseModel
from tests.types import MainConfig

pytest_plugins = ("tests.application.functional.plugins.api_client",)


@pytest.fixture(scope="session")
def main_config() -> MainConfig:
    return get_main_config()


@pytest_asyncio.fixture(scope="session")
async def create_session(main_config: MainConfig) -> AsyncGenerator[async_sessionmaker[AsyncSession], Any]:
    test_engine = create_async_engine(f"{main_config.postgresql.database_url}", echo=False)

    async with test_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)

    _session = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

    yield _session

    async with test_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)


@pytest_asyncio.fixture(scope="session")
async def db_session(create_session: async_sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession, Any]:
    async with create_session() as session:
        yield session
