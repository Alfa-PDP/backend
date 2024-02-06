from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.api.middlewares.main import logger
from app.core import errors
from app.schemas.tasks import (
    TaskCreateSchema,
    TaskExtendedGetSchema,
    TaskGetSchema,
    TaskPartialUpdateSchema,
    TaskWithStatus,
)
from database.models.comment import Comment
from database.models.task import Task


class AbstractTaskRepository(ABC):
    @abstractmethod
    async def get(self, obj_id: UUID) -> TaskGetSchema:
        raise NotImplementedError

    @abstractmethod
    async def get_with_status_and_comments(self, obj_id: UUID) -> TaskExtendedGetSchema:
        raise NotImplementedError

    @abstractmethod
    async def create(self, obj_in: TaskCreateSchema, **kwargs: dict) -> TaskGetSchema:
        raise NotImplementedError

    @abstractmethod
    async def partial_update(self, task_id: UUID, obj_in: TaskPartialUpdateSchema) -> TaskGetSchema:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, obj_id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_idp_id_with_status(self, idp_id: UUID) -> list[TaskWithStatus]:
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_idp_id_with_status_and_comments(self, idp_id: UUID) -> list[TaskExtendedGetSchema]:
        raise NotImplementedError

    @abstractmethod
    async def change_task_status(self, task_id: UUID, status_id: UUID) -> None:
        raise NotImplementedError


class SQLAlchemyTaskRepository(AbstractTaskRepository):
    def __init__(self, session: AsyncSession, model: type[Task] = Task) -> None:
        self._session = session
        self._model = model

    async def get(self, obj_id: UUID) -> TaskGetSchema:
        query = select(Task).where(Task.id == obj_id)
        result = (await self._session.execute(query)).scalars().first()
        if result is None:
            raise errors.TaskNotFoundError
        return TaskGetSchema.model_validate(result)

    async def get_with_status_and_comments(self, obj_id: UUID) -> TaskExtendedGetSchema:
        query = (
            select(Task)
            .where(Task.id == obj_id)
            .options(
                joinedload(Task.status),
                joinedload(Task.comments).joinedload(Comment.user),
                joinedload(Task.task_type),
                joinedload(Task.importance),
            )
        )

        result = (await self._session.execute(query)).scalars().first()
        if result is None:
            raise errors.TaskNotFoundError
        return TaskExtendedGetSchema.model_validate(result)

    async def create(self, obj_in: TaskCreateSchema, **kwargs: dict) -> TaskGetSchema:
        obj_input = obj_in.model_dump()
        db_obj = self._model(**obj_input, **kwargs)
        self._session.add(db_obj)
        await self._session.commit()
        await self._session.refresh(db_obj)
        return TaskGetSchema.model_validate(db_obj)

    async def partial_update(self, task_id: UUID, obj_in: TaskPartialUpdateSchema) -> TaskGetSchema:
        query = update(Task).where(Task.id == task_id).values(**obj_in.model_dump(exclude_unset=True)).returning(Task)
        result = (await self._session.execute(query)).scalars().first()
        await self._session.commit()
        if not result:
            raise errors.TaskNotFoundError
        return TaskGetSchema.model_validate(result)

    async def delete(self, obj_id: UUID) -> None:
        comments_query = delete(Comment).where(Comment.task_id == obj_id).returning(Comment)
        comments_result = (await self._session.execute(comments_query)).scalars().all()

        task_query = delete(Task).where(Task.id == obj_id).returning(Task)
        task_result = (await self._session.execute(task_query)).scalars().first()

        if not task_result:
            raise errors.TaskNotFoundError

        if comments_result:
            for comment in comments_result:
                logger.debug(f"Deleted comment: {comment}")

        await self._session.commit()

    async def get_all_by_idp_id_with_status(self, idp_id: UUID) -> list[TaskWithStatus]:
        query = select(Task).where(Task.idp_id == idp_id).options(joinedload(Task.status))
        results = (await self._session.execute(query)).scalars().all()
        return [TaskWithStatus.model_validate(result) for result in results]

    async def get_all_by_idp_id_with_status_and_comments(self, idp_id: UUID) -> list[TaskExtendedGetSchema]:
        query = (
            select(Task)
            .where(Task.idp_id == idp_id)
            .options(
                joinedload(Task.status),
                joinedload(Task.comments).joinedload(Comment.user),
                joinedload(Task.task_type),
                joinedload(Task.importance),
            )
        )
        results = (await self._session.execute(query)).scalars().unique().all()
        return [TaskExtendedGetSchema.model_validate(result) for result in results]

    async def change_task_status(self, task_id: UUID, status_id: UUID) -> None:
        query = update(Task).where(Task.id == task_id).values(status_id=status_id)
        await self._session.execute(query)
        await self._session.commit()
