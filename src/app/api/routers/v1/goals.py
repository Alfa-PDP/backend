from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies.services import create_goals_service
from app.schemas.goals import GoalSchema
from app.services.goals import GoalsService

router = APIRouter(tags=["Goals"])


@router.get("/goals/{user_id}", response_model=GoalSchema)
async def get_goals_for_user(
    user_id: str,
    goals_service: GoalsService = Depends(create_goals_service),
) -> GoalSchema:
    try:
        goals = await goals_service.get_goals_for_user(user_id)
        return goals
    except HTTPException as error:
        # Прокидываем HTTPException напрямую
        raise error
    except Exception as error:
        # Обработка других исключений
        raise HTTPException(status_code=500, detail=str(error))


@router.post("/goals/{user_id}", response_model=GoalSchema)
async def create_goal_for_user(
    user_id: str,
    goal_data: dict,
    goals_service: GoalsService = Depends(create_goals_service),
) -> GoalSchema:
    try:
        goal = await goals_service.create_goal_for_user(user_id, goal_data)
        return goal
    except ValueError as error:
        raise HTTPException(status_code=404, detail=f"{error}")
    # except LengthError as error:
    #     raise HTTPException(status_code=404, detail=f"{error}")


@router.patch("/goals/{user_id}", response_model=GoalSchema)
async def patch_goal(
    user_id: str,
    updated_data: dict,
    goals_service: GoalsService = Depends(create_goals_service),
) -> GoalSchema:
    try:
        goal = await goals_service.update_goal(user_id, updated_data)
        if goal:
            return goal
    except ValueError as error:
        raise HTTPException(status_code=404, detail=f"{error}")


@router.delete("/goals/{user_id}", status_code=204)
async def delete_goal(
    user_id: str,
    goals_service: GoalsService = Depends(create_goals_service),
) -> None:
    try:
        await goals_service.delete_goal(user_id)
        return
    except ValueError as error:
        raise HTTPException(status_code=404, detail=f"{error}")
    except Exception as error:
        raise HTTPException(status_code=404, detail=f"{error}")
