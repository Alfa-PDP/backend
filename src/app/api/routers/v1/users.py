import logging

from fastapi import APIRouter, status

from app.api.dependencies.auth import AuthorizeUserDep
from app.api.dependencies.repositories import UserRepositoryDep
from app.api.dependencies.services import UsersServiceDep
from app.api.request_model.users import UserQueryParamsDep
from app.schemas.auth import AuthData
from app.schemas.users import UserCreateSchema, UserFilterParams, \
    UserOrderParams, UserWithTaskSchema

router = APIRouter(prefix="/users", tags=["Users"])

logger = logging.getLogger().getChild("user-router")


@router.get(
    "",
    summary="Список сотрудников команды с сортировкой",
    response_model=list[UserWithTaskSchema],
    status_code=status.HTTP_200_OK,
)
async def get_users(users_service: UsersServiceDep,
                    queries: UserQueryParamsDep) -> list[UserWithTaskSchema]:
    logger.debug(f"Getting users with {queries} params")
    filters = UserFilterParams(team_id=queries.team_id)
    order = UserOrderParams(field=queries.order.field,
                            is_desc=queries.order.is_desc)
    return await users_service.get_users(filters, order)


@router.post(
    "",
    summary="Добавление сотрудника",
    status_code=status.HTTP_201_CREATED,
)
async def create_user(user_data: UserCreateSchema,
                      users_repository: UserRepositoryDep) -> None:
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
