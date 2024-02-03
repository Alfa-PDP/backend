from functools import cached_property

from app.schemas.task_status import TaskStatusSlugEnum
from app.schemas.tasks import TaskWithStatus


class UserProgress:
    def __init__(self, tasks: list[TaskWithStatus]) -> None:
        self._tasks = tasks
        self._task_count = len(tasks)

    @cached_property
    def progress(self) -> int:
        completed_tasks = len([task for task in self._tasks if task.status.slug == TaskStatusSlugEnum.completed])
        return self._calculate(completed_tasks, self._task_count)

    def _calculate(self, completed_tasks: int, all_tasks: int) -> int:
        return int(completed_tasks / all_tasks * 100) if completed_tasks else 0

    @property
    def task_count(self) -> int:
        return self._task_count
