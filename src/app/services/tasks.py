from dataclasses import dataclass
from uuid import UUID

from app.repositories.tasks import AbstractTaskRepository
from app.schemas.tasks import TaskSchema


@dataclass
class TasksService:
    _task_repository: AbstractTaskRepository

    async def get_task(self, task_id: UUID) -> TaskSchema:
        return await self._task_repository.get(task_id)
