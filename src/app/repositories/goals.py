from abc import ABC, abstractmethod
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import UserNotFoundError
from app.repositories.users import AbstractUserRepository
from app.schemas.goals import GoalSchema
from database.models.goal import Goal


class AbstractGoalRepository(ABC):
    @abstractmethod
    async def get_goals_for_user(self, user_id: UUID) -> list[GoalSchema]:
        raise NotImplementedError

    @abstractmethod
    async def create_goal_for_user(self, user_id: UUID,
                                   goal_data: dict) -> GoalSchema:
        raise NotImplementedError

    @abstractmethod
    async def update_goal(self, user_id: UUID,
                          updated_data: dict) -> GoalSchema:
        raise NotImplementedError

    @abstractmethod
    async def delete_goal(self, user_id: UUID) -> None:
        raise NotImplementedError


class SqlAlchemyGoalRepository(AbstractGoalRepository):
    def __init__(self, session: AsyncSession,
                 user_repository: AbstractUserRepository):
        self._session = session
        self._user_repository = user_repository

    async def get_goals_for_user(self, user_id: UUID) -> GoalSchema:
        try:
            # Проверка существования пользователя
            user = await self._user_repository.get_by_id(user_id)
            # Запрос целей пользователя
            query = select(Goal).filter(Goal.user_id == user_id)
            result = (await self._session.execute(query)).scalar_one_or_none()
            return GoalSchema.model_validate(result)
        except UserNotFoundError:
            # Обработка ситуации, когда пользователя не найдено
            raise HTTPException(status_code=404,
                                detail=f"User with id {user_id} not found.")
        except Exception as e:
            # Обработка других исключений
            raise e

    async def create_goal_for_user(self, user_id: UUID,
                                   goal_data: dict) -> GoalSchema:
        try:
            # Проверка существования пользователя
            user = await self._user_repository.get_by_id(user_id)
            # Проверка ограничения символов в записях до 500

            # Проверка наличия целей у пользователя
            goal_count = await self._session.scalar(
                select(func.count(Goal.id)).filter(Goal.user_id == user_id))
            if goal_count > 0:
                raise ValueError(f"У пользователя {user_id} уже есть цели")

            # Создание цели
            goal = Goal(**goal_data, user_id=user_id)
            self._session.add(goal)
            await self._session.commit()
            return GoalSchema.model_validate(goal)
        except UserNotFoundError:
            # Обработка ситуации, когда пользователя не найдено
            raise HTTPException(status_code=404,
                                detail=f"User with id {user_id} not found.")
        except Exception as error:
            raise error

    async def update_goal(self, user_id: UUID,
                          updated_data: dict) -> GoalSchema:
        try:
            # Проверка существования пользователя
            user = await self._user_repository.get_by_id(user_id)
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
            return GoalSchema.model_validate(updated_goal.scalars().first())
        except UserNotFoundError:
            # Обработка ситуации, когда пользователя не найдено
            raise HTTPException(status_code=404,
                                detail=f"User with id {user_id} not found.")
        except NoResultFound:
            raise ValueError(
                f"Пользователь с id {user_id} не найден или у него нет целей.")
        except Exception as error:
            raise error

    async def delete_goal(self, user_id: UUID) -> None:
        # Проверка существования пользователя
        user = await self._user_repository.get_by_id(user_id)
        try:
            goal = await self._session.execute(
                select(Goal).filter(Goal.user_id == user_id))
            goal = goal.scalars().first()
            if not goal:
                raise NoResultFound

            await self._session.delete(goal)
        except UserNotFoundError:
            # Обработка ситуации, когда пользователя не найдено
            raise HTTPException(status_code=404,
                                detail=f"User with id {user_id} not found.")
        except NoResultFound:
            raise ValueError(
                f"Пользователь с id {user_id} не найден или у него нет целей.")
        except Exception as error:
            raise error
