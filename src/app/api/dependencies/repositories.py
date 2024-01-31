from typing import Annotated

from fastapi import Depends

from app.api.dependencies.clients import DbSessionDep
from app.repositories.users import AbstractUserRepository, SQLAlchemyUserRepository


def get_user_repository(db_session: DbSessionDep) -> AbstractUserRepository:
    return SQLAlchemyUserRepository(db_session)


UserRepositoryDep = Annotated[AbstractUserRepository, Depends(get_user_repository)]
