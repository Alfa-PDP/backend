from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.tasks import TaskSchema
from database.models.task import Task


class AbstractTaskRepository(ABC):
    ...
