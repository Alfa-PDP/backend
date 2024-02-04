from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.tasks import TaskImportanceSchema, TaskTypeSchema
from database.models.task_importance import Importance
from database.models.task_type import Type


class AbstractTaskAdditionsRepository(ABC):
    @abstractmethod
    async def get_task_types_list(self) -> TaskTypeSchema:
        raise NotImplementedError

    @abstractmethod
    async def get_task_importance_list(self) -> TaskImportanceSchema:
        raise NotImplementedError


class SQLAlchemyTaskAdditionsRepository(AbstractTaskAdditionsRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_task_types_list(self) -> list[TaskTypeSchema]:
        query = select(Type)
        result = await self._session.execute(query)
        return [TaskTypeSchema.model_validate(types) for types in result.scalars()]

    async def get_task_importance_list(self) -> list[TaskImportanceSchema]:
        query = select(Importance)
        result = await self._session.execute(query)
        return [TaskImportanceSchema.model_validate(importance) for importance in result.scalars()]
