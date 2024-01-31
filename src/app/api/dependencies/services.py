from typing import Annotated

from fastapi import Depends

from app.api.dependencies.clients import CacheClientDep, DbSessionDep
from app.api.dependencies.configs import MainConfigDep
from app.api.dependencies.repositories import TeamRepositoryDep, UserRepositoryDep
from app.repositories.tasks import SqlAlchemyTaskRepository
from app.services.auth import AbstractAuthService, FakeAuthService
from app.services.status import StatusService
from app.services.tasks import TasksService
from app.services.users import UsersService


def create_status_service(cache_client: CacheClientDep) -> StatusService:
    return StatusService(cache_client)


def create_users_service(user_repository: UserRepositoryDep) -> UsersService:
    return UsersService(_user_repository=user_repository)


UsersServiceDep = Annotated[UsersService, Depends(create_users_service)]


def create_tasks_service(db_session: DbSessionDep) -> TasksService:
    return TasksService(
        _task_repository=SqlAlchemyTaskRepository(db_session),
    )


def create_auth_service(config: MainConfigDep, team_repository: TeamRepositoryDep) -> AbstractAuthService:
    if not config.project.is_production:
        return FakeAuthService(_team_repository=team_repository)
    return FakeAuthService(
        _team_repository=team_repository
    )  # TODO поменять на реальную авторизацию при внедрении сервиса


AuthServiceDep = Annotated[AbstractAuthService, Depends(create_auth_service)]
