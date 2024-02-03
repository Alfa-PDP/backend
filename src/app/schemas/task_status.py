from enum import Enum, IntEnum, StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TaskStatusSlugEnum(StrEnum):
    new = "new"
    completed = "completed"
    in_progress = "in_progress"
    canceled = "canceled"


class TaskStatusDescriptionEnum(StrEnum):
    new = "Новая"
    completed = "Выполнена"
    in_progress = "В работе"
    canceled = "Отменена"


class TaskStatusWeight(IntEnum):
    new = 4
    completed = 3
    in_progress = 2
    canceled = 1


class TaskStatusEnum(Enum):
    new = TaskStatusSlugEnum.new, TaskStatusDescriptionEnum.new, TaskStatusWeight.new
    completed = TaskStatusSlugEnum.completed, TaskStatusDescriptionEnum.completed, TaskStatusWeight.completed
    in_progress = TaskStatusSlugEnum.in_progress, TaskStatusDescriptionEnum.in_progress, TaskStatusWeight.in_progress
    canceled = TaskStatusSlugEnum.canceled, TaskStatusDescriptionEnum.canceled, TaskStatusWeight.canceled

    @property
    def slug(self) -> TaskStatusSlugEnum:
        return self.value[0]

    @property
    def description(self) -> TaskStatusDescriptionEnum:
        return self.value[1]

    @property
    def weight(self) -> TaskStatusWeight:
        return self.value[2]


class TaskStatusSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    slug: TaskStatusSlugEnum
    description: TaskStatusDescriptionEnum
    weight: TaskStatusWeight


class ChangeTaskStatus(BaseModel):
    description: TaskStatusDescriptionEnum
