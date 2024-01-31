from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import UserNotInTeamError
from database.models.team import Team
from database.models.user_team import UserTeam

CompletedTasks = int
AllTasks = int


class AbstractTeamRepository(ABC):
    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> Team:
        raise NotImplementedError


class SQLAlchemyTeamRepository(AbstractTeamRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_user_id(self, user_id: UUID) -> Team:
        query = select(Team).join(UserTeam, onclause=and_(UserTeam.user_id == user_id, UserTeam.team_id == Team.id))

        result = (await self._session.execute(query)).scalar_one_or_none()

        if not result:
            raise UserNotInTeamError

        return result
