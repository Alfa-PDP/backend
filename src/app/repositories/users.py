from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import column_property

from app.core import errors
from app.schemas.task_status import StatusSlugEnum
from app.schemas.users import CreateUserSchema, GetUserSchema, UserFilterParams
from database.models.idp import Idp
from database.models.status import Status
from database.models.task import Task
from database.models.user import User
from database.models.user_team import UserTeam

CompletedTasks = int
AllTasks = int


class AbstractUserRepository(ABC):
    @abstractmethod
    async def get_all(self, filters: UserFilterParams) -> list[GetUserSchema]:
        raise NotImplementedError

    @abstractmethod
    async def create(self, user_data: CreateUserSchema) -> None:
        raise NotImplementedError

    @abstractmethod
    async def count_completed_tasks_for_users(
        self, users: tuple[UUID, ...]
    ) -> Sequence[tuple[UUID, CompletedTasks, AllTasks]]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> GetUserSchema:
        raise NotImplementedError


class SQLAlchemyUserRepository(AbstractUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_all(self, filters: UserFilterParams) -> list[GetUserSchema]:
        User.team_id = column_property(UserTeam.team_id, expire_on_flush=True)
        query = select(User).join(UserTeam)

        if filters.team_id:
            query = query.filter(UserTeam.team_id == filters.team_id)

        results = (await self._session.execute(query)).scalars().all()

        return [GetUserSchema.model_validate(result) for result in results]

    async def create(self, user_data: CreateUserSchema) -> None:
        user = User(**user_data.model_dump())
        self._session.add(user)

    async def count_completed_tasks_for_users(
        self, users: tuple[UUID, ...]
    ) -> Sequence[tuple[UUID, CompletedTasks, AllTasks]]:
        completed_tasks = func.count(Task.id).filter(Status.slug == StatusSlugEnum.completed)
        all_tasks = func.count(Task.id)

        query = (
            select(User.id, completed_tasks, all_tasks)
            .join(Idp, onclause=Idp.user_id == User.id, isouter=True)
            .join(Task, onclause=Task.idp_id == Idp.id, isouter=True)
            .join(Status, onclause=Status.id == Task.status_id, isouter=True)
            .where(User.id.in_(users))
            .group_by(User.id)
        )

        results = (await self._session.execute(query)).tuples().all()
        return results

    async def get_by_id(self, user_id: UUID) -> GetUserSchema:
        User.team_id = column_property(UserTeam.team_id, expire_on_flush=True)
        query = select(User).where(User.id == user_id).join(UserTeam)
        result = (await self._session.execute(query)).scalar_one_or_none()

        if not result:
            raise errors.UserNotFoundError

        return GetUserSchema.model_validate(result)

