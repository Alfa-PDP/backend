from functools import cached_property

from app.schemas.task_status import StatusSlugEnum
from app.schemas.tasks import TaskWithStatusSchema


class UserProgress:
    def __init__(self, tasks: list[TaskWithStatusSchema]) -> None:
        self._tasks = tasks

    @cached_property
    def progress(self) -> int:
        all_tasks = len(self._tasks)
        completed_tasks = len([task for task in self._tasks if
                               task.status.slug == StatusSlugEnum.completed])
        return self.calculate(completed_tasks, all_tasks)

    @classmethod
    def calculate(cls, completed_tasks: int, all_tasks: int) -> int:
        return int(completed_tasks / all_tasks * 100) if completed_tasks else 0
