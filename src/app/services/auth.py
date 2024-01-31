from abc import ABC, abstractmethod
from uuid import UUID

from app.schemas.auth import AuthData


class AbstractAuthService(ABC):
    @abstractmethod
    async def authorize_user(self, user_id: UUID) -> AuthData:
        raise NotImplementedError


class FakeAuthService(AbstractAuthService):
    async def authorize_user(self, user_id: UUID) -> AuthData:
        return AuthData(user_id=user_id, is_leader=True)
