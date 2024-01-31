from datetime import date
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel


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


class TaskSchema(BaseModel):
    id: UUID
    name: str
    description: str
    task_type: TaskType
    start_time: date
    end_time: date
    importance: ImportanceType
    idp_id: UUID
    status_id: UUID