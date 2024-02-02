from typing import Annotated

from fastapi import Depends

from app.api.dependencies.clients import CacheClientDep, DbSessionDep
from app.api.dependencies.configs import MainConfigDep
from app.api.dependencies.repositories import (IDPRepositoryDep,
                                               TaskRepositoryDep,
                                               TeamRepositoryDep,
                                               UserRepositoryDep)
from app.repositories.goals import SqlAlchemyGoalRepository
from app.services.auth import AbstractAuthService, FakeAuthService
from app.services.goals import GoalsService
from app.services.idp import IDPService
from app.services.status import StatusService
from app.services.tasks import TasksService
from app.services.users import UsersService


def create_status_service(cache_client: CacheClientDep) -> StatusService:
    return StatusService(cache_client)


def create_users_service(user_repository: UserRepositoryDep) -> UsersService:
    return UsersService(_user_repository=user_repository)


UsersServiceDep = Annotated[UsersService, Depends(create_users_service)]


def create_tasks_service(tasks_repository: TaskRepositoryDep) -> TasksService:
    return TasksService(_task_repository=tasks_repository)


def create_auth_service(config: MainConfigDep,
                        team_repository: TeamRepositoryDep) -> AbstractAuthService:
    if not config.project.is_production:
        return FakeAuthService(_team_repository=team_repository)
    return FakeAuthService(
        _team_repository=team_repository
    )  # TODO поменять на реальную авторизацию при внедрении сервиса


AuthServiceDep = Annotated[AbstractAuthService, Depends(create_auth_service)]


def get_idp_service(
        idp_repository: IDPRepositoryDep, user_repository: UserRepositoryDep,
        tasks_repository: TaskRepositoryDep
) -> IDPService:
    return IDPService(
        _idp_repository=idp_repository, _user_repository=user_repository,
        _tasks_repository=tasks_repository
    )


def create_goals_service(db_session: DbSessionDep,
                         user_repository: UserRepositoryDep) -> GoalsService:
    return GoalsService(
        _goal_repository=SqlAlchemyGoalRepository(db_session, user_repository),
    )


IDPServiceDep = Annotated[IDPService, Depends(get_idp_service)]
