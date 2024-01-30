import logging  # noqa
from typing import Annotated  # noqa
from uuid import UUID

from fastapi import APIRouter, Depends, status  # noqa

from app.api.dependencies.services import create_tasks_service
from app.schemas.tasks import TaskSchema
from app.services.tasks import TasksService

router = APIRouter(prefix="/tasks", tags=["Tasks"])

logger = logging.getLogger().getChild("task-router")

TasksServiceDep = Annotated[TasksService, Depends(create_tasks_service())]


@router.get("/{task_id}", summary="Получить задачу по id", response_model=TaskSchema, status_code=status.HTTP_200_OK)
async def _get_task(task_id: UUID, tasks_service: TasksServiceDep) -> TaskSchema:
    logger.debug("Get api status")
    return await tasks_service.get_task(task_id=task_id)
