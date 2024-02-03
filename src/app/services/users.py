from dataclasses import dataclass
from typing import Generator

from app.domain.user_progress import UserProgress
from app.repositories.users import AbstractUserRepository
from app.schemas.users import GetUserWithProgressSchema, UserFilterParams, UserOrderParams, UserWithTasksSchema


@dataclass
class UsersService:
    _user_repository: AbstractUserRepository

    async def get_users_with_progress(
        self,
        filters: UserFilterParams,
        order: UserOrderParams,
    ) -> list[GetUserWithProgressSchema]:
        users = await self._user_repository.get_all_with_tasks(filters)

        users_generator = self._generate_users_with_progress(users)
        sorted_users = self._sort_users(users_generator, order)

        return sorted_users

    def _generate_users_with_progress(
        self,
        users: list[UserWithTasksSchema],
    ) -> Generator[GetUserWithProgressSchema, None, None]:
        for user in users:
            user_progress = UserProgress(user.tasks)
            user_with_progress = GetUserWithProgressSchema(
                **user.model_dump(),
                task_count=user_progress.task_count,
                task_progress=user_progress.progress,
            )
            yield user_with_progress

    def _sort_users(
        self,
        users_generator: Generator[GetUserWithProgressSchema, None, None],
        order: UserOrderParams,
    ) -> list[GetUserWithProgressSchema]:
        result = sorted(
            users_generator,
            key=lambda user: getattr(user, order.sort_by, user.family_name),
            reverse=order.is_desc,
        )
        return result
