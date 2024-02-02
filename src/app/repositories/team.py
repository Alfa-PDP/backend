from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import errors
from app.schemas.team import TeamSchema
from database.models.team import Team
from database.models.user_team import UserTeam


class AbstractTeamRepository(ABC):
    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> TeamSchema:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, team_id: UUID) -> TeamSchema:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[TeamSchema]:
        raise NotImplementedError


class SQLAlchemyTeamRepository(AbstractTeamRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_user_id(self, user_id: UUID) -> TeamSchema:
        query = select(Team).join(UserTeam, onclause=and_(UserTeam.user_id == user_id, UserTeam.team_id == Team.id))

        result = (await self._session.execute(query)).scalar_one_or_none()

        if not result:
            raise errors.UserNotInTeamError

        return TeamSchema.model_validate(result)

    async def get_by_id(self, team_id: UUID) -> TeamSchema:
        result = (await self._session.execute(select(Team).where(Team.id == team_id))).scalar_one_or_none()

        if not result:
            raise errors.TeamNotFoundError

        return TeamSchema.model_validate(result)

    async def get_all(self) -> list[TeamSchema]:
        results = (await self._session.execute(select(Team))).scalars().all()
        return [TeamSchema.model_validate(result) for result in results]
