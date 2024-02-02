from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.goals import AbstractGoalRepository, SqlAlchemyGoalRepository
from app.schemas.goals import GoalSchema


class GoalsService:
    def __init__(self, _goal_repository: AbstractGoalRepository) -> None:
        self._goal_repository = _goal_repository

    async def get_goals_for_user(self, user_id: UUID) -> GoalSchema:
        return await self._goal_repository.get_goals_for_user(user_id)

    async def create_goal_for_user(self, user_id: UUID, goal_data: dict) -> GoalSchema:
        return await self._goal_repository.create_goal_for_user(user_id, goal_data)

    async def update_goal(self, user_id: UUID, updated_data: dict) -> GoalSchema:
        return await self._goal_repository.update_goal(user_id, updated_data)

    async def delete_goal(self, user_id: UUID) -> None:
        await self._goal_repository.delete_goal(user_id)


async def create_goals_service(session: AsyncSession) -> GoalsService:
    goal_repository = SqlAlchemyGoalRepository(session)
    return GoalsService(goal_repository)
