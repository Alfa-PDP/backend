from datetime import date
from enum import StrEnum
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
    education = "Образование"
    hardskills = "Hardskills"
    softskills = "Softskills"
    tasks = "Задания"
    kpi = "KPI"
    other = "Другое"


class ImportanceType(StrEnum):
    high = "Высокая"
    medium = "Средняя"
    easy = "Низкая"


class TaskGetSchema(TaskBase):
    id: UUID
    idp_id: UUID
    task_type: TaskType
    importance: ImportanceType
    status_id: UUID
    status: TaskStatusSchema


class TaskCreateSchema(TaskBase):
    idp_id: UUID
    importance: ImportanceType
    task_type: TaskType
    status_id: UUID


class TaskUpdateSchema(TaskBase):
    id: UUID
    task_type: TaskType
    importance: ImportanceType


class TaskWithCommentsGetSchema(TaskGetSchema):
    comments: list[GetTaskCommentSchema]
