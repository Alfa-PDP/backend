from app.api.dependencies.clients import CacheClientDep, DbSessionDep
from app.repositories.tasks import SqlAlchemyTaskRepository
from app.repositories.users import SqlAlchemyUserRepository
from app.services.status import StatusService
from app.services.tasks import TasksService
from app.services.users import UsersService


def create_status_service(cache_client: CacheClientDep) -> StatusService:
    return StatusService(cache_client)


def create_users_service(db_session: DbSessionDep) -> UsersService:
    return UsersService(
        _user_repository=SqlAlchemyUserRepository(db_session),
    )


def create_tasks_service(db_session: DbSessionDep) -> TasksService:
    return TasksService(
        _task_repository=SqlAlchemyTaskRepository(db_session),
    )
