from abc import ABC, abstractmethod  # noqa
from uuid import UUID

from sqlalchemy import select  # noqa
from sqlalchemy.ext.asyncio import AsyncSession  # noqa

from app.schemas.tasks import TaskSchema  # noqa
from database.models.task import Task  # noqa


class AbstractTaskRepository(ABC):
    @abstractmethod
    async def get(self, obj_id: UUID) -> TaskSchema:
        raise NotImplementedError

    @abstractmethod
    async def put(self, obj_in: TaskSchema, **kwargs: dict) -> TaskSchema:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, db_obj: TaskSchema) -> TaskSchema:
        raise NotImplementedError


class SqlAlchemyTaskRepository(AbstractTaskRepository):
    def __init__(self, session: AsyncSession, model: Task = Task) -> None:
        self._session = session
        self._model = model

    async def get(self, obj_id: UUID) -> TaskSchema:
        obj = await self._session.execute(select(self._model).where(self._model.id == obj_id))
        return obj.scalars().first()

    async def put(self, obj_in: TaskSchema, **kwargs: dict) -> TaskSchema:
        obj_input = obj_in.dict()
        db_obj = self._model(**obj_input, **kwargs)
        self._session.add(db_obj)
        await self._session.commit()
        await self._session.refresh(db_obj)
        return db_obj

    async def delete(self, db_obj: TaskSchema) -> TaskSchema:
        await self._session.delete(db_obj)
        await self._session.commit()
        return db_obj
