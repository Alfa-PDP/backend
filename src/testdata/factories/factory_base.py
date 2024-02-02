from typing import Generic, TypeVar

from faker import Faker
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory

from testdata.db_connection import async_session_maker, db_session

Model = TypeVar("Model")


class BaseSQLAlchemyFactory(Generic[Model], SQLAlchemyFactory[Model]):
    __faker__ = Faker(locale="en_US")
    __is_base_factory__ = True

    @classmethod
    def build_all(cls) -> list[Model]:
        raise NotImplementedError

    @classmethod
    async def add_all(cls, data: list[Model]) -> None:
        async with db_session(async_session_maker) as session:
            session.add_all(data)
            await session.commit()

    @classmethod
    async def add(cls, data: Model) -> None:
        async with db_session(async_session_maker) as session:
            session.add(data)
            await session.commit()
