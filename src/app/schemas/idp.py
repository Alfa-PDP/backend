import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.schemas.tasks import TaskWithStatus


class IDPCreateSchema(BaseModel):
    user_id: UUID
    start_date: datetime.date
    end_date: datetime.date
    year: int


class IDPFilter(BaseModel):
    year: int


class IDPGetSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    start_date: datetime.date
    end_date: datetime.date
    year: int


class IDPGetExtendedSchema(IDPGetSchema):
    model_config = ConfigDict(from_attributes=True)

    name: str
    family_name: str
    middle_name: str
    position: str
    avatar: str | None
    email: str | None
    phone_number: str | None
    telegram: str | None
    team_id: UUID
    task_count: int
    task_progress: int
    tasks: list[TaskWithStatus]


class IDPProgressSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    task_count: int
    task_progress: int
