from dataclasses import dataclass
from typing import Sequence
from uuid import UUID

from app.domain.user_progress import UserProgress
from app.repositories.users import AbstractUserRepository
from app.schemas.users import UserFilterParams, UserOrderParams, UserWithTaskSchema


@dataclass
class UsersService:
    _user_repository: AbstractUserRepository

    async def get_users(self, filters: UserFilterParams, order: UserOrderParams) -> list[UserWithTaskSchema]:
        users = await self._user_repository.get_all(filters)
        users_ids = {user.id: [0, 0] for user in users}
        user_ids_with_tasks = await self._user_repository.count_completed_tasks_for_users(tuple(users_ids.keys()))
        self._aggregate_users_info(users_ids, user_ids_with_tasks)

        users_gen = (
            UserWithTaskSchema(
                **user.model_dump(), task_count=users_ids[user.id][0], task_progress=users_ids[user.id][1]
            )
            for user in users
        )

        result = sorted(
            users_gen,
            key=lambda user: getattr(user, order.field, user.family_name),
            reverse=order.is_desc,
        )

        return result

    def _aggregate_users_info(
            self, users_ids: dict[UUID, list[int]], user_ids_with_tasks: Sequence[tuple[UUID, int, int]]
    ) -> dict[UUID, list[int]]:
        for info in user_ids_with_tasks:
            user_id = info[0]
            completed_tasks = info[1]
            all_tasks = info[2]

            users_ids[user_id][0] = all_tasks
            users_ids[user_id][1] = UserProgress.calculate(completed_tasks, all_tasks)

        return users_ids
