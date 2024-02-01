import logging  # noqa
from typing import Annotated  # noqa
from uuid import UUID

from fastapi import APIRouter, Depends, status  # noqa

from app.api.dependencies.services import create_tasks_service
from app.schemas.tasks import TaskCreateSchema, TaskGetSchema, TaskUpdateSchema
from app.services.tasks import TasksService

router = APIRouter(prefix="/tasks", tags=["Tasks"])

logger = logging.getLogger().getChild("task-router")

TasksServiceDep = Annotated[TasksService, Depends(create_tasks_service)]


@router.get("", summary="Получить задачу по id", response_model=TaskGetSchema, status_code=status.HTTP_200_OK)
async def _get_task(task_id: UUID, tasks_service: TasksServiceDep) -> TaskGetSchema:
    logger.debug("Getting Task by id")
    return await tasks_service.get_task(task_id=task_id)


@router.post("", summary="Создание задачи", response_model=TaskGetSchema, status_code=status.HTTP_201_CREATED)
async def _create_task(user_id: UUID, task_data: TaskCreateSchema, tasks_service: TasksServiceDep) -> TaskGetSchema:
    logger.debug("Create Task")
    return await tasks_service.create_task(user_id, task_data)


@router.put("", summary="Редактирование поста", response_model=TaskGetSchema, status_code=status.HTTP_201_CREATED)
async def _update_task(task_id: UUID, task_data: TaskUpdateSchema, tasks_service: TasksServiceDep) -> TaskGetSchema:
    logger.debug("Update Task")
    return await tasks_service.update_task(task_id, task_data)


@router.delete("", summary="Удаление задачи", status_code=status.HTTP_204_NO_CONTENT)
async def _delete_task(task_id: UUID, tasks_service: TasksServiceDep) -> dict:
    logger.debug("Delete Task")
    return await tasks_service.delete(task_id)
