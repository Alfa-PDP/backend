from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import TaskStatusNotFoundError
from app.schemas.task_status import TaskStatusSchema
from database.models.status import Status


class AbstractTaskStatusRepository(ABC):
    @abstractmethod
    async def get(self, status_id: UUID) -> TaskStatusSchema:
        raise NotImplementedError


class SQLAlchemyTaskStatusRepository(AbstractTaskStatusRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, status_id: UUID) -> TaskStatusSchema:
        query = select(Status).where(Status.id == status_id)
        result = (await self._session.execute(query)).scalars().first()
        if not result:
            raise TaskStatusNotFoundError
        return TaskStatusSchema.model_validate(result)
