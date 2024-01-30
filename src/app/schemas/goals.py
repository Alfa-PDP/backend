from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class GoalSchema(BaseModel):
    id: UUID
    user_id: UUID
    goal_name: str
    employee_side_plus: Optional[str]
    employee_side_minus: Optional[str]

    class Config:
        orm_mode = True
        from_attributes = True
