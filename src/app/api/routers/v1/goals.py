from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies.services import create_goals_service
from app.services.goals import GoalsService
from app.schemas.goals import GoalSchema

router = APIRouter()


@router.get("/goals/{user_id}", response_model=list[GoalSchema])
async def get_goals_for_user(
    user_id: str,
    goals_service: GoalsService = Depends(create_goals_service),
):
    goals = await goals_service.get_goals_for_user(user_id)
    return goals


@router.post("/goals/{user_id}", response_model=GoalSchema)
async def create_goal_for_user(
    user_id: str,
    goal_data: dict,
    goals_service: GoalsService = Depends(create_goals_service),
):
    goal = await goals_service.create_goal_for_user(user_id, goal_data)
    return goal


@router.put("/goals/{goal_id}", response_model=GoalSchema)
async def update_goal(
    goal_id: str,
    updated_data: dict,
    goals_service: GoalsService = Depends(create_goals_service),
):
    goal = await goals_service.update_goal(goal_id, updated_data)
    if goal:
        return goal
    raise HTTPException(status_code=404, detail="Goal not found")


@router.delete("/goals/{goal_id}", status_code=204, deprecated=True)
async def delete_goal(
    goal_id: str,
    goals_service: GoalsService = Depends(create_goals_service),
):
    try:
        # Тут пока всё отладка.
        await goals_service.delete_goal(goal_id)
        return {"message": "Goal deleted successfully"}
    except Exception as err:
        return {"message": f"error - {err}"}
