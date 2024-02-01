from datetime import date
from enum import StrEnum

from pydantic import BaseModel, ConfigDict

from app.schemas.task_status import TaskStatusSchema


class TaskBase(BaseModel):
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
    id: int
    idp_id: int
    task_type: TaskType
    importance: ImportanceType
    status_id: int
    items: TaskStatusSchema
    # schema: list[TaskCommentSchema]


class TaskCreateSchema(TaskBase):
    idp_id: int
    importance: ImportanceType
    task_type: TaskType
    status_id: int


class TaskUpdateSchema(TaskBase):
    id: int
    task_type: TaskType
    importance: ImportanceType


class TaskWithStatusSchema(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    status: TaskStatusSchema
