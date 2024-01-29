from dataclasses import dataclass

from app.repositories.tasks import AbstractTaskRepository
from app.schemas.tasks import TaskSchema


@dataclass
class TasksService:
    ...
