import logging
from uuid import UUID

from fastapi import APIRouter, status

from app.api.dependencies.auth import AuthorizeUserDep
from app.api.dependencies.repositories import UserRepositoryDep
from app.api.dependencies.services import GoalsServiceDep, TasksServiceDep, UsersServiceDep
from app.api.request_model.users import UserQueryParamsDep, UserTasksQueryParamsDep
from app.schemas.auth import AuthData
from app.schemas.goals import GoalSchema
from app.schemas.idp import IDPFilter
from app.schemas.tasks import TaskExtendedGetSchema
from app.schemas.users import CreateUserSchema, GetUserWithProgressSchema, UserFilterParams, UserOrderParams

router = APIRouter(prefix="/users", tags=["Users"])

logger = logging.getLogger().getChild("user-router")


@router.get(
    "",
    summary="Список сотрудников команды с сортировкой",
    response_model=list[GetUserWithProgressSchema],
    status_code=status.HTTP_200_OK,
)
async def get_users(users_service: UsersServiceDep, queries: UserQueryParamsDep) -> list[GetUserWithProgressSchema]:
    logger.debug(f"Getting users with {queries} params")
    filters = UserFilterParams(team_id=queries.team_id, year=queries.year)
    order = UserOrderParams(sort_by=queries.sort_by, order=queries.order)
    return await users_service.get_users_with_progress(filters, order)


@router.post(
    "",
    summary="Добавление сотрудника",
    status_code=status.HTTP_201_CREATED,
)
async def create_user(user_data: CreateUserSchema, users_repository: UserRepositoryDep) -> None:
    logger.debug(f"Create user: {user_data}")
    return await users_repository.create(user_data)


@router.get(
    "/me",
    summary="Информация о текущем пользователе",
    response_model=AuthData,
    status_code=status.HTTP_200_OK,
)
async def get_user(auth_data: AuthorizeUserDep) -> AuthData:
    return auth_data


@router.get(
    "/{user_id}/tasks",
    summary="Задачи сотрудника",
    response_model=list[TaskExtendedGetSchema],
    status_code=status.HTTP_200_OK,
)
async def get_user_tasks(
    user_id: UUID, query_param: UserTasksQueryParamsDep, tasks_service: TasksServiceDep
) -> list[TaskExtendedGetSchema]:
    logger.debug(f"Get user's {user_id} tasks.")
    filters = IDPFilter(year=query_param.year)
    return await tasks_service.get_all_by_user_id(user_id, filters)


@router.get(
    "/{user_id}/goals",
    summary="Цели сотрудника",
    response_model=GoalSchema,
    status_code=status.HTTP_200_OK,
)
async def get_goals_for_user(
    user_id: UUID,
    goals_service: GoalsServiceDep,
) -> GoalSchema:
    goals = await goals_service.get_goal_for_user(user_id)
    return goals
