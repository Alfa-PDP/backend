import logging
from uuid import UUID

from fastapi import APIRouter, status

from app.api.dependencies.repositories import (
    TaskAdditionsRepositoryDep,
    TaskCommentRepositoryDep,
    TaskRepositoryDep,
    TaskStatusRepositoryDep,
)
from app.api.dependencies.services import TasksServiceDep
from app.schemas.comment import CreateTaskCommentSchema, GetTaskCommentSchema
from app.schemas.task_status import ChangeTaskStatus, TaskStatusSchema
from app.schemas.tasks import (
    TaskCreateSchema,
    TaskExtendedGetSchema,
    TaskImportanceSchema,
    TaskTypeSchema,
    TaskUpdateSchema,
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])

logger = logging.getLogger().getChild("task-router")


@router.get(
    "/status",
    summary="Получить список статусов для задач",
    status_code=status.HTTP_200_OK,
    response_model=list[TaskStatusSchema],
)
async def get_status_list(
        status_repository: TaskStatusRepositoryDep,
) -> list[TaskStatusSchema]:
    status_list = await status_repository.get_status_list()
    return status_list


@router.get(
    "/task_types",
    summary="Получить список типов задач",
    status_code=status.HTTP_200_OK,
    response_model=list[TaskTypeSchema],
)
async def get_task_types_list(
        task_types_repository: TaskAdditionsRepositoryDep,
) -> list[TaskTypeSchema]:
    types_list = await task_types_repository.get_task_types_list()
    return types_list


@router.get(
    "/task_importance",
    summary="Получить список важности задач",
    status_code=status.HTTP_200_OK,
    response_model=list[TaskImportanceSchema],
)
async def get_task_importance_list(
        task_importance_repository: TaskAdditionsRepositoryDep,
) -> list[TaskImportanceSchema]:
    importance_list = await task_importance_repository.get_task_importance_list()
    return importance_list


@router.get(
    "/{task_id}",
    summary="Получить задачу по id",
    response_model=TaskExtendedGetSchema,
    status_code=status.HTTP_200_OK,
)
async def _get_task(task_id: UUID, tasks_repository: TaskRepositoryDep) -> TaskExtendedGetSchema:
    logger.debug("Getting Task by id")
    return await tasks_repository.get_with_status_and_comments(obj_id=task_id)


@router.post(
    "",
    summary="Создание задачи",
    response_model=TaskExtendedGetSchema,
    status_code=status.HTTP_201_CREATED,
)
async def _create_task(
    task_data: TaskCreateSchema,
    tasks_service: TasksServiceDep,
) -> TaskExtendedGetSchema:
    logger.debug("Create Task")
    return await tasks_service.create(task_data)


@router.put(
    "",
    summary="Редактирование реквизитов задачи",
    response_model=TaskExtendedGetSchema,
    status_code=status.HTTP_201_CREATED,
)
async def _update_task(
    task_data: TaskUpdateSchema,
    tasks_service: TasksServiceDep,
) -> TaskExtendedGetSchema:
    logger.debug("Update Task")
    return await tasks_service.update(task_data)


@router.delete(
    "/{task_id}",
    summary="Удаление задачи",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def _delete_task(
    task_id: UUID,
    tasks_repository: TaskRepositoryDep,
) -> None:
    logger.debug("Delete Task")
    await tasks_repository.delete(task_id)


@router.get(
    "/{task_id}/comments",
    summary="Комментарии к задаче сотрудника",
    response_model=list[GetTaskCommentSchema],
    status_code=status.HTTP_200_OK,
)
async def get_task_comments(task_id: UUID, comment_repository: TaskCommentRepositoryDep) -> list[GetTaskCommentSchema]:
    logger.debug(f"Getting task {task_id} comments")
    return await comment_repository.get_all_by_task_id(task_id)


@router.post(
    "/{task_id}/comments",
    summary="Добавить комментарий к задаче",
    status_code=status.HTTP_201_CREATED,
)
async def create_task_comment(
    task_id: UUID,
    comment_data: CreateTaskCommentSchema,
    task_comment_repository: TaskCommentRepositoryDep,
) -> None:
    logger.debug(f"Creating comment {comment_data} for {task_id} task id")
    await task_comment_repository.create(task_id, comment_data)


@router.patch(
    "/{task_id}/status",
    summary="Изменить статус задачи",
    status_code=status.HTTP_201_CREATED,
)
async def change_task_status(
    task_id: UUID,
    task_status_data: ChangeTaskStatus,
    tasks_service: TasksServiceDep,
) -> None:
    logger.debug(f"Changing status for task id {task_id}")
    await tasks_service.change_task_status(task_id, task_status_data)
