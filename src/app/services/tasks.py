from dataclasses import dataclass
from uuid import UUID

from app.repositories.tasks import AbstractTaskRepository
from app.schemas.tasks import TaskGetSchema


@dataclass
class TasksService:
    _task_repository: AbstractTaskRepository

    async def get_task(self, task_id: UUID) -> TaskGetSchema:
        return await self._task_repository.get(task_id)

    async def delete(self, task_id: UUID) -> None:
        return await self._task_repository.delete(task_id)
