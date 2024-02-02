from dataclasses import dataclass
from uuid import UUID

from app.repositories.tasks import AbstractTaskRepository
from app.schemas.tasks import TaskCreateSchema, TaskGetSchema, TaskUpdateSchema


@dataclass
class TasksService:
    _task_repository: AbstractTaskRepository

    async def get_task(self, task_id: UUID) -> TaskGetSchema:
        return await self._task_repository.get(task_id)

    async def create_task(self, user_id: UUID, task_data: TaskCreateSchema) -> TaskGetSchema:
        ...

    async def update_task(self, task_id: UUID, task_data: TaskUpdateSchema) -> TaskGetSchema:
        ...

    async def delete(self, task_id: UUID) -> dict:
        return await self._task_repository.delete(task_id)
