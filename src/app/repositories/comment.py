from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy import asc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager

from app.schemas.comment import CreateTaskCommentSchema, GetTaskCommentSchema
from database.models.comment import Comment


class AbstractTaskCommentRepository(ABC):
    @abstractmethod
    async def create(self, task_id: UUID,
                     comment_data: CreateTaskCommentSchema) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_task_id(self, task_id: UUID) -> list[
        GetTaskCommentSchema]:
        raise NotImplementedError


class SQLAlchemyTaskCommentRepository(AbstractTaskCommentRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, task_id: UUID,
                     comment_data: CreateTaskCommentSchema) -> None:
        comment = Comment(**comment_data.model_dump(), task_id=task_id)
        self._session.add(comment)
        await self._session.commit()

    async def get_all_by_task_id(self, task_id: UUID) -> list[
        GetTaskCommentSchema]:
        query = (
            select(Comment)
            .join(Comment.user)
            .where(Comment.task_id == task_id)
            .order_by(asc(Comment.created_at))
            .options(contains_eager(Comment.user))
        )

        results = (await self._session.execute(query)).scalars().all()
        return [GetTaskCommentSchema.model_validate(result) for result in
                results]
