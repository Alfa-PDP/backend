from typing import Annotated

from fastapi import Depends

from app.api.dependencies.clients import CacheClientDep
from app.api.dependencies.configs import MainConfigDep
from app.api.dependencies.repositories import (
    GoalRepositoryDep,
    IDPRepositoryDep,
    TaskRepositoryDep,
    TaskStatusRepositoryDep,
    TeamRepositoryDep,
    UserRepositoryDep,
)
from app.services.api_status import APIStatusService
from app.services.auth import AbstractAuthService, FakeAuthService
from app.services.goals import GoalsService
from app.services.idp import IDPService
from app.services.tasks import TasksService
from app.services.users import UsersService


def create_api_status_service(cache_client: CacheClientDep) -> APIStatusService:
    return APIStatusService(cache_client)


def create_users_service(user_repository: UserRepositoryDep) -> UsersService:
    return UsersService(_user_repository=user_repository)


UsersServiceDep = Annotated[UsersService, Depends(create_users_service)]


def create_tasks_service(
    tasks_repository: TaskRepositoryDep,
    idp_repository: IDPRepositoryDep,
    task_status_repository: TaskStatusRepositoryDep,
) -> TasksService:
    return TasksService(
        _task_repository=tasks_repository,
        _idp_repository=idp_repository,
        _task_status_repository=task_status_repository,
    )


TasksServiceDep = Annotated[TasksService, Depends(create_tasks_service)]


def create_auth_service(config: MainConfigDep, team_repository: TeamRepositoryDep) -> AbstractAuthService:
    if not config.project.is_production:
        return FakeAuthService(_team_repository=team_repository)
    return FakeAuthService(
        _team_repository=team_repository
    )  # TODO поменять на реальную авторизацию при внедрении сервиса


AuthServiceDep = Annotated[AbstractAuthService, Depends(create_auth_service)]


def get_idp_service(
    idp_repository: IDPRepositoryDep, user_repository: UserRepositoryDep, tasks_repository: TaskRepositoryDep
) -> IDPService:
    return IDPService(
        _idp_repository=idp_repository,
        _user_repository=user_repository,
        _tasks_repository=tasks_repository,
    )


IDPServiceDep = Annotated[IDPService, Depends(get_idp_service)]


def get_goals_service(
    user_repository: UserRepositoryDep,
    goals_repository: GoalRepositoryDep,
) -> GoalsService:
    return GoalsService(
        _goal_repository=goals_repository,
        _user_repository=user_repository,
    )


GoalsServiceDep = Annotated[GoalsService, Depends(get_goals_service)]
