from abc import ABC, abstractmethod  # noqa

from sqlalchemy import select  # noqa
from sqlalchemy.ext.asyncio import AsyncSession  # noqa

from app.schemas.tasks import TaskSchema  # noqa
from database.models.task import Task  # noqa


class AbstractTaskRepository(ABC):
    ...
