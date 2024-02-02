from enum import StrEnum
from typing import assert_never
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class StatusSlugEnum(StrEnum):
    completed = "completed"
    in_progress = "in_progress"
    canceled = "canceled"

    @property
    def weight(self) -> int:
        match self:
            case StatusSlugEnum.completed:
                return 3
            case StatusSlugEnum.in_progress:
                return 2
            case StatusSlugEnum.canceled:
                return 1
            case _:
                assert_never(self)

                
class TaskStatusSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    slug: StatusSlugEnum
    description: str
    weight: float
