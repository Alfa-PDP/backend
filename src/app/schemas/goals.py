from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class GoalSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    goal_name: str = Field(max_length=500)
    employee_side_plus: Optional[str] = Field(max_length=500)
    employee_side_minus: Optional[str] = Field(max_length=500)


class CreateGoal(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: UUID
    goal_name: str = Field(max_length=500)
    employee_side_plus: Optional[str] = Field(max_length=500)
    employee_side_minus: Optional[str] = Field(max_length=500)


class UpdateGoal(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    goal_name: str | None = Field(None, max_length=500)
    employee_side_plus: str | None = Field(None, max_length=500)
    employee_side_minus: str | None = Field(None, max_length=500)
