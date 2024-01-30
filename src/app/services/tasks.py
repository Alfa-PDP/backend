from dataclasses import dataclass

from app.repositories.tasks import SqlAlchemyTaskRepository
from app.schemas.tasks import TaskSchema


@dataclass
class TasksService:
    _task_repository: SqlAlchemyTaskRepository

    async def get_task(self) -> TaskSchema:
        return await self._task_repository.get(TaskSchema.id)
