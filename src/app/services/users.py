from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.repositories.users import AbstractUserRepository
from app.schemas.users import UserSchema


@dataclass
class UsersService:
    _user_repository: AbstractUserRepository

    async def get_all_users(self) -> list[UserSchema]:
        return await self._user_repository.get_all()
