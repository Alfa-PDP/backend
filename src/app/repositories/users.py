from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.users import UserSchema
from database.models.user import User


class AbstractUserRepository(ABC):
    @abstractmethod
    async def get_all(self) -> list[UserSchema]:
        raise NotImplementedError


class SqlAlchemyUserRepository(AbstractUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_all(self) -> list[UserSchema]:
        result = await self._session.execute(select(User))
        users = result.fetchall()

        return [UserSchema.model_validate(user) for user in users]
