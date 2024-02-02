from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from app.repositories.team import AbstractTeamRepository
from app.schemas.auth import AuthData


class AbstractAuthService(ABC):
    @abstractmethod
    async def authorize_user(self, user_id: UUID) -> AuthData:
        raise NotImplementedError


@dataclass
class FakeAuthService(AbstractAuthService):
    _team_repository: AbstractTeamRepository

    async def authorize_user(self, user_id: UUID) -> AuthData:
        team = await self._team_repository.get_by_user_id(user_id)
        return AuthData(user_id=user_id, team_id=team.id,
                        is_leader=team.leader_id == user_id)
