from datetime import date
from enum import Enum, StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.schemas.comment import GetTaskCommentSchema
from app.schemas.task_status import TaskStatusSchema


class TaskBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: str
    start_time: date
    end_time: date


class TaskType(StrEnum):
    education = "Обучение"
    hardskills = "Hard skills"
    softskills = "Soft skills"


class ImportanceType(StrEnum):
    high = "Высокая"
    medium = "Средняя"
    easy = "Низкая"


class TaskTypeEnum(Enum):
    education = TaskType.education
    hardskills = TaskType.hardskills
    softskills = TaskType.softskills

    @property
    def name(self) -> TaskType:
        return self.value


class TaskImportanceEnum(Enum):
    high = ImportanceType.high
    medium = ImportanceType.medium
    easy = ImportanceType.easy

    @property
    def name(self) -> ImportanceType:
        return self.value


class TaskTypeSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: TaskTypeEnum


class TaskImportanceSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: TaskImportanceEnum


class TaskGetSchema(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    idp_id: UUID
    status_id: UUID


class TaskCreateSchema(TaskBase):
    idp_id: UUID
    importance_id: UUID
    task_type_id: UUID
    status_id: UUID


class TaskUpdateSchema(TaskBase):
    id: UUID
    task_type_id: UUID
    importance_id: UUID


class TaskWithStatus(TaskGetSchema):
    status: TaskStatusSchema


class TaskWithComments(TaskGetSchema):
    comments: list[GetTaskCommentSchema]


class TaskWithType(TaskGetSchema):
    task_type: TaskTypeSchema


class TaskWithImportance(TaskGetSchema):
    importance: TaskImportanceSchema


class TaskExtendedGetSchema(TaskWithStatus, TaskWithComments, TaskWithType, TaskWithImportance):
    ...
