from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.schemas.tasks import TaskCreateSchema, TaskGetSchema, TaskUpdateSchema, TaskWithCommentsGetSchema
from database.models.comment import Comment
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
    async def delete(self, obj_id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_idp_id_with_status(self, idp_id: UUID) -> list[TaskGetSchema]:
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_idp_id_with_status_and_comments(self, idp_id: UUID) -> list[TaskWithCommentsGetSchema]:
        raise NotImplementedError


class SQLAlchemyTaskRepository(AbstractTaskRepository):
    def __init__(self, session: AsyncSession, model: type[Task] = Task) -> None:
        self._session = session
        self._model = model

    async def get(self, obj_id: UUID) -> TaskGetSchema:
        obj = await self._session.execute(select(self._model).where(self._model.id == obj_id))
        result = obj.scalars().first()
        if result is None:
            raise FileNotFoundError
        return TaskGetSchema.model_validate(result)

    async def create(self, obj_in: TaskCreateSchema, **kwargs: dict) -> TaskGetSchema:
        obj_input = obj_in.model_dump()
        db_obj = self._model(**obj_input, **kwargs)
        self._session.add(db_obj)
        await self._session.commit()
        await self._session.refresh(db_obj)
        return TaskGetSchema.model_validate(db_obj)

    async def update(self, obj_id: UUID, obj_in: TaskUpdateSchema) -> TaskGetSchema:
        db_obj = await self._session.execute(select(self._model).where(self._model.id == obj_id))
        obj_data = db_obj.scalars().first()
        if obj_data is None:
            raise FileNotFoundError
        update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, obj_in[field])
            self._session.add(db_obj)
        await self._session.commit()
        return TaskGetSchema.model_validate(obj_data)

    async def delete(self, obj_id: UUID) -> None:
        await self._session.delete(obj_id)
        await self._session.commit()

    async def get_all_by_idp_id_with_status(self, idp_id: UUID) -> list[TaskGetSchema]:
        query = select(Task).where(Task.idp_id == idp_id).options(joinedload(Task.status))
        results = (await self._session.execute(query)).scalars().all()
        return [TaskGetSchema.model_validate(result) for result in results]

    async def get_all_by_idp_id_with_status_and_comments(self, idp_id: UUID) -> list[TaskWithCommentsGetSchema]:
        query = (
            select(Task)
            .where(Task.idp_id == idp_id)
            .options(
                joinedload(Task.status),
                joinedload(Task.comments).joinedload(Comment.user),
            )
        )
        results = (await self._session.execute(query)).scalars().unique().all()
        return [TaskWithCommentsGetSchema.model_validate(result) for result in results]
