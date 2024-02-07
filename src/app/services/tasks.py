from dataclasses import dataclass
from uuid import UUID

from app.repositories.idp import AbstractIDPRepository
from app.repositories.tasks import AbstractTaskRepository
from app.repositories.tasks_status import AbstractTaskStatusRepository
from app.schemas.idp import IDPFilter
from app.schemas.task_status import ChangeTaskStatus
from app.schemas.tasks import TaskCreateSchema, TaskExtendedGetSchema, TaskUpdateSchema


@dataclass
class TasksService:
    _task_repository: AbstractTaskRepository
    _idp_repository: AbstractIDPRepository
    _task_status_repository: AbstractTaskStatusRepository

    async def get_all_by_user_id(self, user_id: UUID, filters: IDPFilter) -> list[TaskExtendedGetSchema]:
        user_current_idp = await self._idp_repository.get_by_user_and_filter(user_id, filters)
        tasks = await self._task_repository.get_all_by_idp_id_with_status_and_comments(user_current_idp.id)
        return tasks

    async def create(self, data: TaskCreateSchema) -> TaskExtendedGetSchema:
        await self._idp_repository.get(data.idp_id)
        await self._task_status_repository.get(data.status_id)
        task = await self._task_repository.create(data)
        return await self._task_repository.get_with_status_and_comments(task.id)

    async def update(self, task_id: UUID, data: TaskUpdateSchema) -> TaskExtendedGetSchema:
        task = await self._task_repository.update(task_id, data)
        return await self._task_repository.get_with_status_and_comments(task.id)

    async def change_task_status(self, task_id: UUID, task_status_data: ChangeTaskStatus) -> None:
        task = await self._task_repository.get(task_id)
        status = await self._task_status_repository.get_by_description(task_status_data.description)
        await self._task_repository.change_task_status(task.id, status.id)
