import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.api.dependencies.repositories import TaskCommentRepositoryDep  # noqa
from app.api.dependencies.services import create_tasks_service
from app.schemas.comment import CreateTaskCommentSchema, GetTaskCommentSchema
from app.schemas.tasks import TaskSchema
from app.services.tasks import TasksService

router = APIRouter(prefix="/tasks", tags=["Tasks"])

logger = logging.getLogger().getChild("task-router")

TasksServiceDep = Annotated[TasksService, Depends(create_tasks_service)]


@router.get("/{task_id}", summary="Получить задачу по id", response_model=TaskSchema, status_code=status.HTTP_200_OK)
async def _get_task(task_id: UUID, tasks_service: TasksServiceDep) -> TaskSchema:
    logger.debug("Get api status")
    return await tasks_service.get_task(task_id=task_id)


@router.get(
    "/{task_id}/comments",
    summary="Комментарии к задаче сотрудника",
    response_model=list[GetTaskCommentSchema],
    status_code=status.HTTP_200_OK,
)
async def get_comments(task_id: UUID, comment_repository: TaskCommentRepositoryDep) -> list[GetTaskCommentSchema]:
    logger.debug(f"Getting task {task_id} comments")
    return await comment_repository.get_all_by_task_id(task_id)


@router.post(
    "/{task_id}/comments",
    summary="Добавить комментарий к задаче",
    status_code=status.HTTP_201_CREATED,
)
async def create_comment(
    task_id: UUID,
    comment_data: CreateTaskCommentSchema,
    task_comment_repository: TaskCommentRepositoryDep,
) -> None:
    logger.debug(f"Creating comment {comment_data} for {task_id} task id")
    await task_comment_repository.create(task_id, comment_data)
