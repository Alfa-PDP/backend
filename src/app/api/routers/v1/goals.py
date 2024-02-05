import logging
from uuid import UUID

from fastapi import APIRouter, status

from app.api.dependencies.services import GoalsServiceDep
from app.schemas.goals import CreateGoal, GoalSchema, UpdateGoal

router = APIRouter(tags=["Goals"], prefix="/goals")

logger = logging.getLogger().getChild("goals-router")


@router.post(
    "",
    summary="Создать цель",
    response_model=GoalSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_goal_for_user(
    goal_data: CreateGoal,
    goals_service: GoalsServiceDep,
) -> GoalSchema:
    """
    Создание цели для пользователя.

    Args:
        - goal_data (CreateGoal): Данные для создания цели.
        - goals_service (GoalsServiceDep): Сервис для работы с целями.

    Returns:
        - GoalSchema: Информация о созданной цели.
    """
    logger.debug("Creating goal")
    goal = await goals_service.create_goal_for_user(goal_data)
    return goal


@router.patch(
    "/{goal_id}",
    summary="Редактировать цель",
    response_model=GoalSchema,
    status_code=status.HTTP_200_OK,
)
async def patch_goal(
    goal_id: UUID,
    updated_data: UpdateGoal,
    goals_service: GoalsServiceDep,
) -> GoalSchema:
    """
    Редактирование цели.

    Args:
        - goal_id (UUID): Идентификатор цели.
        - updated_data (UpdateGoal): Обновленные данные цели.
        - goals_service (GoalsServiceDep): Сервис для работы с целями.

    Returns:
        - GoalSchema: Информация о цели после редактирования.
    """
    logger.debug(f"Updating goal {goal_id}")
    goal = await goals_service.update_goal(goal_id, updated_data)
    return goal


@router.delete(
    "/{goal_id}",
    summary="Удалить цель",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_goal(
    goal_id: UUID,
    goals_service: GoalsServiceDep,
) -> None:
    """
    Удаление цели.

    Args:
        - goal_id (UUID): Идентификатор цели.
        - goals_service (GoalsServiceDep): Сервис для работы с целями.
    """
    logger.debug(f"Deleting goal {goal_id}")
    await goals_service.delete_goal(goal_id)
