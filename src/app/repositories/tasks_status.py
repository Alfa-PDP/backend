from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import errors
from app.schemas.task_status import TaskStatusDescriptionEnum, TaskStatusSchema
from database.models.status import Status


class AbstractTaskStatusRepository(ABC):
    @abstractmethod
    async def get(self, status_id: UUID) -> TaskStatusSchema:
        raise NotImplementedError

    @abstractmethod
    async def update(self, status: TaskStatusSchema) -> TaskStatusSchema:
        raise NotImplementedError

    @abstractmethod
    async def get_by_description(self, description: TaskStatusDescriptionEnum) -> TaskStatusSchema:
        raise NotImplementedError

    @abstractmethod
    async def get_status_list(self) -> TaskStatusSchema:
        raise NotImplementedError


class SQLAlchemyTaskStatusRepository(AbstractTaskStatusRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, status_id: UUID) -> TaskStatusSchema:
        query = select(Status).where(Status.id == status_id)
        result = (await self._session.execute(query)).scalars().first()
        if not result:
            raise errors.TaskStatusNotFoundError
        return TaskStatusSchema.model_validate(result)

    async def update(self, status: TaskStatusSchema) -> TaskStatusSchema:
        query = select(Status).where(Status.id == status.id)
        task_status = (await self._session.execute(query)).scalars().first()
        if not task_status:
            raise errors.TaskStatusNotFoundError

        for key, value in status.model_dump(exclude_unset=True).items():
            setattr(task_status, key, value)

        return TaskStatusSchema.model_validate(task_status)

    async def get_by_description(self, description: TaskStatusDescriptionEnum) -> TaskStatusSchema:
        query = select(Status).where(Status.description == description)
        task_status = (await self._session.execute(query)).scalars().first()
        if not task_status:
            raise errors.TaskStatusNotFoundError
        return TaskStatusSchema.model_validate(task_status)

    async def get_status_list(self) -> list[TaskStatusSchema]:
        query = select(Status)
        result = await self._session.execute(query)
        return [TaskStatusSchema.model_validate(status) for status in result.scalars()]
