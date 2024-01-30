from app.api.dependencies.clients import CacheClientDep, DbSessionDep
from app.repositories.goals import SqlAlchemyGoalRepository
from app.repositories.users import SqlAlchemyUserRepository
from app.services.goals import GoalsService
from app.services.status import StatusService
from app.services.users import UsersService


def create_status_service(cache_client: CacheClientDep) -> StatusService:
    return StatusService(cache_client)


def create_users_service(db_session: DbSessionDep) -> UsersService:
    return UsersService(
        _user_repository=SqlAlchemyUserRepository(db_session),
    )


def create_goals_service(db_session: DbSessionDep) -> GoalsService:
    return GoalsService(
        _goal_repository=SqlAlchemyGoalRepository(db_session),
    )
