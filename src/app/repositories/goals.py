from abc import ABC

from sqlalchemy import select, func
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import LengthError
from app.schemas.goals import GoalSchema
from database.models.goal import Goal
from database.models.user import User


class AbstractGoalRepository(ABC):
    async def get_goals_for_user(self, user_id: str) -> list[GoalSchema]:
        raise NotImplementedError

    async def create_goal_for_user(self, user_id: str,
                                   goal_data: dict) -> GoalSchema:
        raise NotImplementedError

    async def update_goal(self, goal_id: int,
                          updated_data: dict) -> GoalSchema:
        raise NotImplementedError

    async def delete_goal(self, goal_id: int) -> None:
        raise NotImplementedError


class SqlAlchemyGoalRepository(AbstractGoalRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_goals_for_user(self, user_id: str) -> list[GoalSchema]:
        try:
            # Проверка существования пользователя
            user = await self._session.get(User, user_id)
            if not user:
                raise NoResultFound

            # Запрос целей пользователя
            query = select(Goal).filter(Goal.user_id == user_id)
            result = await self._session.execute(query)
            goals = result.scalars().all()

            return [GoalSchema.from_orm(goal) for goal in goals]
        except NoResultFound:
            raise ValueError(f"Пользователь с id {user_id} не найден.")
        except Exception as e:
            raise e

    async def create_goal_for_user(self, user_id: str,
                                   goal_data: dict) -> GoalSchema:
        try:
            # Проверка существования пользователя
            user = await self._session.get(User, user_id)
            if not user:
                raise NoResultFound

            # Проверка ограничения символов в записях до 500
            for key, value in goal_data.items():
                if isinstance(value, str) and len(value) > 500:
                    raise LengthError(
                        f"Превышено ограничение на длину записи для поля {key}")

            # Проверка наличия целей у пользователя
            goal_count = await self._session.scalar(
                select(func.count(Goal.id)).filter(Goal.user_id == user_id)
            )

            if goal_count > 0:
                raise ValueError(f"У пользователя {user_id} уже есть цели")

            # Создание цели
            goal = Goal(**goal_data, user_id=user_id)
            self._session.add(goal)
            await self._session.commit()
            return GoalSchema.from_orm(goal)
        except NoResultFound:
            raise ValueError(f"Пользователь с id {user_id} не найден.")
        except LengthError as error:
            await self._session.rollback()
            raise error
        except Exception as error:
            await self._session.rollback()
            raise error

    async def update_goal(self, user_id: str,
                          updated_data: dict) -> GoalSchema:
        try:
            # Проверка существования пользователя
            user = await self._session.get(User, user_id)
            if not user:
                raise NoResultFound

            # Проверка существования цели пользователя
            goal = await self._session.execute(
                select(Goal).filter(Goal.user_id == user_id))
            goal = goal.scalars().first()
            if not goal:
                raise NoResultFound

            # Обновление данных цели
            for key, value in updated_data.items():
                setattr(goal, key, value)

            # Коммит изменений
            await self._session.commit()

            # Обновленный объект Goal
            updated_goal = await self._session.execute(
                select(Goal).filter(Goal.user_id == user_id))
            return GoalSchema.from_orm(updated_goal.scalars().first())
        except NoResultFound:
            raise ValueError(
                f"Пользователь с id {user_id} не найден или у него нет целей.")
        except Exception as error:
            await self._session.rollback()
            raise error

    async def delete_goal(self, user_id: str) -> None:
        try:
            goal = await self._session.execute(
                select(Goal).filter(Goal.user_id == user_id))
            goal = goal.scalars().first()

            if not goal:
                raise NoResultFound

            await self._session.delete(goal)
        except NoResultFound:
            raise ValueError(
                f"Пользователь с id {user_id} не найден или у него нет целей.")
