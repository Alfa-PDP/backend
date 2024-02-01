from enum import StrEnum, auto
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class StatusSlugEnum(StrEnum):
    created = "created"
    completed = auto()
    canceled = auto()
    in_progress = "in-progress"


class TaskStatusSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    slug: StatusSlugEnum
    description: str
    weight: float
