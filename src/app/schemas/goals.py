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
