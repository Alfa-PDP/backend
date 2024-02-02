from dataclasses import dataclass
from uuid import UUID

from app.repositories.idp import AbstractIDPRepository
from app.repositories.tasks import AbstractTaskRepository
from app.schemas.idp import IDPFilter
from app.schemas.tasks import TaskCreateSchema, TaskGetSchema, TaskUpdateSchema, TaskWithCommentsGetSchema


@dataclass
class TasksService:
    _task_repository: AbstractTaskRepository
    _idp_repository: AbstractIDPRepository

    async def get_task(self, task_id: UUID) -> TaskGetSchema:
        return await self._task_repository.get(task_id)

    async def create_task(self, user_id: UUID, task_data: TaskCreateSchema) -> TaskGetSchema:
        ...

    async def update_task(self, task_id: UUID, task_data: TaskUpdateSchema) -> TaskGetSchema:
        ...

    async def delete(self, task_id: UUID) -> dict:
        return await self._task_repository.delete(task_id)

    async def get_all_by_user_id(self, user_id: UUID, filters: IDPFilter) -> list[TaskWithCommentsGetSchema]:
        user_current_idp = await self._idp_repository.get_by_user_and_filter(user_id, filters)
        tasks = await self._task_repository.get_all_by_idp_id_with_status_and_comments(user_current_idp.id)
        return tasks
