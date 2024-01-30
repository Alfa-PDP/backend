from typing import Optional
from pydantic import BaseModel
from uuid import UUID


class GoalSchema(BaseModel):
    id: UUID
    user_id: UUID
    goal_name: str
    employee_side_plus: Optional[str]
    employee_side_minus: Optional[str]

    class Config:
        orm_mode = True
        from_attributes = True
