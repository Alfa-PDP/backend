from functools import cached_property

from app.schemas.tasks import TaskWithStatusSchema


class UserProgress:
    def __init__(self, tasks: list[TaskWithStatusSchema]) -> None:
        self._tasks = tasks

    @cached_property
    def user_progress(self) -> int:
        all_tasks = len(self._tasks)
        completed_tasks = len([task for task in self._tasks if task.status.slug == "completed"])  # TODO: use enum
        return self.calculate_user_progress(completed_tasks, all_tasks)

    @classmethod
    def calculate_user_progress(cls, completed_tasks: int, all_tasks: int) -> int:
        return int(completed_tasks / all_tasks * 100) if completed_tasks else 0
