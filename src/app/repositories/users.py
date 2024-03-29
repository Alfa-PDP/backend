from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import column_property, contains_eager

from app.core import errors
from app.schemas.users import CreateUserSchema, GetUserSchema, UserFilterParams, UserWithTasksSchema
from database.models.idp import Idp
from database.models.status import Status
from database.models.task import Task
from database.models.user import User
from database.models.user_team import UserTeam

CompletedTasks = int
AllTasks = int


class AbstractUserRepository(ABC):
    @abstractmethod
    async def get_all_with_tasks(self, filters: UserFilterParams) -> list[UserWithTasksSchema]:
        raise NotImplementedError

    @abstractmethod
    async def create(self, user_data: CreateUserSchema) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> GetUserSchema:
        raise NotImplementedError


class SQLAlchemyUserRepository(AbstractUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_all_with_tasks(self, filters: UserFilterParams) -> list[UserWithTasksSchema]:
        User.team_id = column_property(UserTeam.team_id, expire_on_flush=True)
        query = (
            select(User)
            .join(UserTeam)
            .join(Idp, onclause=and_(Idp.user_id == User.id, Idp.year == filters.year))
            .join(User.tasks, isouter=True)
            .join(Status, onclause=Status.id == Task.status_id)
            .options(
                contains_eager(User.tasks, Task.status),
            )
        )

        if filters.team_id:
            query = query.filter(UserTeam.team_id == filters.team_id)

        results = (await self._session.execute(query)).scalars().unique().all()

        return [UserWithTasksSchema.model_validate(result) for result in results]

    async def create(self, user_data: CreateUserSchema) -> None:
        user = User(**user_data.model_dump())
        self._session.add(user)

    async def get_by_id(self, user_id: UUID) -> GetUserSchema:
        User.team_id = column_property(UserTeam.team_id, expire_on_flush=True)
        query = select(User).where(User.id == user_id).join(UserTeam)
        result = (await self._session.execute(query)).scalar_one_or_none()

        if not result:
            raise errors.UserNotFoundError

        return GetUserSchema.model_validate(result)
