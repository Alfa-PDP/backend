from typing import Annotated

from fastapi import Depends

from app.api.dependencies.clients import DbSessionDep
from app.repositories.comment import AbstractTaskCommentRepository, SQLAlchemyTaskCommentRepository
from app.repositories.goals import AbstractGoalRepository, SqlAlchemyGoalRepository
from app.repositories.idp import AbstractIDPRepository, SQLAlchemyIDPRepository
from app.repositories.task_additions import AbstractTaskAdditionsRepository, SQLAlchemyTaskAdditionsRepository
from app.repositories.tasks import AbstractTaskRepository, SQLAlchemyTaskRepository
from app.repositories.tasks_status import AbstractTaskStatusRepository, SQLAlchemyTaskStatusRepository
from app.repositories.team import AbstractTeamRepository, SQLAlchemyTeamRepository
from app.repositories.users import AbstractUserRepository, SQLAlchemyUserRepository


def get_user_repository(db_session: DbSessionDep) -> AbstractUserRepository:
    return SQLAlchemyUserRepository(db_session)


UserRepositoryDep = Annotated[AbstractUserRepository, Depends(get_user_repository)]


def get_team_repository(db_session: DbSessionDep) -> AbstractTeamRepository:
    return SQLAlchemyTeamRepository(db_session)


TeamRepositoryDep = Annotated[AbstractTeamRepository, Depends(get_team_repository)]


def get_idp_repository(db_session: DbSessionDep) -> AbstractIDPRepository:
    return SQLAlchemyIDPRepository(db_session)


IDPRepositoryDep = Annotated[AbstractIDPRepository, Depends(get_idp_repository)]


def get_task_repository(db_session: DbSessionDep) -> AbstractTaskRepository:
    return SQLAlchemyTaskRepository(db_session)


TaskRepositoryDep = Annotated[AbstractTaskRepository, Depends(get_task_repository)]


def get_comment_repository(db_session: DbSessionDep) -> AbstractTaskCommentRepository:
    return SQLAlchemyTaskCommentRepository(db_session)


TaskCommentRepositoryDep = Annotated[AbstractTaskCommentRepository, Depends(get_comment_repository)]


def get_task_status_repository(db_session: DbSessionDep) -> AbstractTaskStatusRepository:
    return SQLAlchemyTaskStatusRepository(db_session)


TaskStatusRepositoryDep = Annotated[AbstractTaskStatusRepository, Depends(get_task_status_repository)]


def get_goal_repository(db_session: DbSessionDep) -> AbstractGoalRepository:
    return SqlAlchemyGoalRepository(db_session)


GoalRepositoryDep = Annotated[AbstractGoalRepository, Depends(get_goal_repository)]


def get_task_additions_repository(db_session: DbSessionDep) -> AbstractTaskAdditionsRepository:
    return SQLAlchemyTaskAdditionsRepository(db_session)


TaskAdditionsRepositoryDep = Annotated[AbstractTaskAdditionsRepository, Depends(get_task_additions_repository)]
