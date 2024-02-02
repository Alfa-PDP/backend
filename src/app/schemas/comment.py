from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class GetTaskCommentSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    task_id: UUID
    text: str
    created_at: datetime
    updated_at: datetime
    user: "GetUserTaskCommentSchema"


class GetUserTaskCommentSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    family_name: str
    avatar: str | None


class CreateTaskCommentSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    user_id: UUID
    text: str
    created_at: datetime
    updated_at: datetime
