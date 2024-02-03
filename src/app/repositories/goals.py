from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import errors
from app.schemas.goals import CreateGoal, GoalSchema, UpdateGoal
from database.models.goal import Goal


class AbstractGoalRepository(ABC):
    @abstractmethod
    async def get_by_user_id_or_none(self, user_id: UUID) -> GoalSchema | None:
        raise NotImplementedError

    @abstractmethod
    async def create_goal_for_user(self, goal_data: CreateGoal) -> GoalSchema:
        raise NotImplementedError

    @abstractmethod
    async def update_goal(self, goal_id: UUID, updated_data: UpdateGoal) -> GoalSchema:
        raise NotImplementedError

    @abstractmethod
    async def delete_goal(self, goal_id: UUID) -> None:
        raise NotImplementedError


class SqlAlchemyGoalRepository(AbstractGoalRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_user_id_or_none(self, user_id: UUID) -> GoalSchema | None:
        try:
            query = select(Goal).where(Goal.user_id == user_id)
            result = (await self._session.execute(query)).scalars().first()
            return GoalSchema.model_validate(result) if result else None
        except IntegrityError:
            raise errors.ApplicationError

    async def create_goal_for_user(self, goal_data: CreateGoal) -> GoalSchema:
        try:
            goal = Goal(**goal_data.model_dump())
            self._session.add(goal)
            await self._session.commit()
            return GoalSchema.model_validate(goal)
        except IntegrityError:
            raise errors.ApplicationError

    async def update_goal(self, goal_id: UUID, updated_data: UpdateGoal) -> GoalSchema:
        try:
            result = await self._session.execute(select(Goal).filter(Goal.id == goal_id))
            goal: Optional[Goal] = result.scalars().first()
            if not goal:
                raise errors.GoalNotFoundError
            for key, value in updated_data.model_dump(exclude_unset=True).items():
                setattr(goal, key, value)
            await self._session.commit()
            return GoalSchema.model_validate(goal)
        except IntegrityError:
            raise errors.ApplicationError

    async def delete_goal(self, goal_id: UUID) -> None:
        try:
            result = await self._session.execute(select(Goal).filter(Goal.id == goal_id))
            goal = result.scalars().first()
            if not goal:
                raise errors.GoalNotFoundError
            await self._session.delete(goal)
            await self._session.commit()
        except IntegrityError:
            raise errors.ApplicationError
