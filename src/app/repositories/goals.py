from abc import ABC
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from uuid import UUID
from database.models.goal import Goal
from app.schemas.goals import GoalSchema


class AbstractGoalRepository(ABC):
    async def get_goals_for_user(self, user_id: str) -> list[GoalSchema]:
        raise NotImplementedError

    async def create_goal_for_user(self, user_id: str, goal_data: dict) -> GoalSchema:
        raise NotImplementedError

    async def update_goal(self, goal_id: int, updated_data: dict) -> GoalSchema:
        raise NotImplementedError

    async def delete_goal(self, goal_id: int) -> None:
        raise NotImplementedError


class SqlAlchemyGoalRepository(AbstractGoalRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_goals_for_user(self, user_id: str) -> list[GoalSchema]:
        # Проверяем, является ли user_id строкой в формате UUID
        try:
            user_id_uuid = UUID(user_id)
        except ValueError:
            # Если не удалось преобразовать в UUID, предполагаем, что это строка
            query = select(Goal).filter(Goal.user_id == user_id)
        else:
            # Если успешно преобразован в UUID, используем его в запросе
            query = select(Goal).filter(Goal.user_id == user_id_uuid)

        result = await self._session.execute(query)
        goals = result.scalars().all()
        return [GoalSchema.from_orm(goal) for goal in goals]

    async def create_goal_for_user(self, user_id: str, goal_data: dict) -> GoalSchema:
        # Реализация создания цели пользователя в базе данных
        goal = Goal(**goal_data, user_id=user_id)
        self._session.add(goal)
        await self._session.commit()
        return GoalSchema.from_orm(goal)

    async def update_goal(self, id: str, updated_data: dict) -> GoalSchema:
        # Реализация редактирования цели в базе данных
        goal = await self._session.get(Goal, id)
        if goal:
            for key, value in updated_data.items():
                setattr(goal, key, value)
            await self._session.commit()
            return GoalSchema.from_orm(goal)
        return None

    async def delete_goal(self, id: str) -> None:
        goal = await self._session.get(Goal, id)
        if goal:
            await self._session.delete(goal)
            await self._session.flush()
            return None
        else:
            raise ValueError(f"Цели с id {id} не найдены!")