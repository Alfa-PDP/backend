import logging
from uuid import UUID

from fastapi import APIRouter, status

from app.api.dependencies.repositories import TaskCommentRepositoryDep, TaskRepositoryDep
from app.schemas.comment import CreateTaskCommentSchema, GetTaskCommentSchema
from app.schemas.tasks import TaskCreateSchema, TaskGetSchema, TaskUpdateSchema

router = APIRouter(prefix="/tasks", tags=["Tasks"])

logger = logging.getLogger().getChild("task-router")


@router.get("/{task_id}", summary="Получить задачу по id", response_model=TaskGetSchema, status_code=status.HTTP_200_OK)
async def _get_task(task_id: UUID, tasks_service: TaskRepositoryDep) -> TaskGetSchema:
    logger.debug("Getting Task by id")
    return await tasks_service.get(task_id=task_id)


@router.post("", summary="Создание задачи", response_model=TaskGetSchema, status_code=status.HTTP_201_CREATED)
async def _create_task(user_id: UUID, task_data: TaskCreateSchema, tasks_service: TaskRepositoryDep) -> TaskGetSchema:
    logger.debug("Create Task")
    return await tasks_service.create(task_data)


@router.put("", summary="Редактирование поста", response_model=TaskGetSchema, status_code=status.HTTP_201_CREATED)
async def _update_task(task_id: UUID, task_data: TaskUpdateSchema, tasks_service: TaskRepositoryDep) -> TaskGetSchema:
    logger.debug("Update Task")
    return await tasks_service.update(task_id, task_data)


@router.delete("", summary="Удаление задачи", status_code=status.HTTP_204_NO_CONTENT)
async def _delete_task(task_id: UUID, tasks_service: TaskRepositoryDep) -> None:
    logger.debug("Delete Task")
    await tasks_service.delete(task_id)


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
