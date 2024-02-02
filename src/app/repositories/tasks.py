from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager

from app.schemas.tasks import TaskCreateSchema, TaskGetSchema, TaskUpdateSchema, TaskWithStatusSchema
from database.models.task import Task


class AbstractTaskRepository(ABC):
    @abstractmethod
    async def get(self, obj_id: UUID) -> TaskGetSchema:
        raise NotImplementedError

    @abstractmethod
    async def create(self, obj_in: TaskCreateSchema, **kwargs: dict) -> TaskGetSchema:
        raise NotImplementedError

    @abstractmethod
    async def update(self, obj_id: UUID, obj_in: TaskUpdateSchema) -> TaskGetSchema:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, obj_id: UUID) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_idp_id_with_status(self, idp_id: UUID) -> list[TaskWithStatusSchema]:
        raise NotImplementedError


class SQLAlchemyTaskRepository(AbstractTaskRepository):
    def __init__(self, session: AsyncSession, model: type[Task] = Task) -> None:
        self._session = session
        self._model = model

    async def get(self, obj_id: UUID) -> TaskGetSchema:
        obj = await self._session.execute(select(self._model).where(self._model.id == obj_id))
        return obj.scalars().first()

    async def create(self, obj_in: TaskCreateSchema, **kwargs: dict) -> TaskGetSchema:
        obj_input = obj_in.model_dump()
        db_obj = self._model(**obj_input, **kwargs)
        self._session.add(db_obj)
        await self._session.commit()
        await self._session.refresh(db_obj)
        return db_obj

    async def update(self, obj_id: UUID, obj_in: TaskUpdateSchema) -> TaskGetSchema:
        ...

    async def delete(self, obj_id: UUID) -> dict:
        await self._session.delete(obj_id)
        await self._session.commit()
        return {"details": f"Task {obj_id} deleted."}

    async def get_all_by_idp_id_with_status(self, idp_id: UUID) -> list[TaskWithStatusSchema]:
        query = select(Task).join(Task.status).where(Task.idp_id == idp_id).options(contains_eager(Task.status))
        results = (await self._session.execute(query)).scalars().all()
        return [TaskWithStatusSchema.model_validate(result) for result in results]
