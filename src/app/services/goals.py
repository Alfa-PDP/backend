from dataclasses import dataclass
from uuid import UUID

from app.core import errors
from app.repositories.goals import AbstractGoalRepository
from app.repositories.users import AbstractUserRepository
from app.schemas.goals import CreateGoal, GoalSchema, UpdateGoal


@dataclass
class GoalsService:
    _goal_repository: AbstractGoalRepository
    _user_repository: AbstractUserRepository

    async def get_goal_for_user(self, user_id: UUID) -> GoalSchema:
        await self._user_repository.get_by_id(user_id)
        user_goal = await self._goal_repository.get_by_user_id_or_none(user_id)
        if not user_goal:
            raise errors.GoalNotFounError
        return user_goal

    async def create_goal_for_user(self, goal_data: CreateGoal) -> GoalSchema:
        await self._user_repository.get_by_id(goal_data.user_id)
        user_goal = await self._goal_repository.get_by_user_id_or_none(goal_data.user_id)
        if user_goal:
            raise errors.GoalAlreadyExistsError
        return await self._goal_repository.create_goal_for_user(goal_data)

    async def update_goal(self, goal_id: UUID, updated_data: UpdateGoal) -> GoalSchema:
        return await self._goal_repository.update_goal(goal_id, updated_data)

    async def delete_goal(self, goal_id: UUID) -> None:
        await self._goal_repository.delete_goal(goal_id)
