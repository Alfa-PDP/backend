from app.schemas.task_status import TaskStatusEnum
from database.models.status import Status
from testdata.factories.common_data import status_ids
from testdata.factories.factory_base import BaseSQLAlchemyFactory


class TaskStatusFactory(BaseSQLAlchemyFactory[Status]):
    @classmethod
    def build_all(cls) -> list[Status]:
        return [
            cls.build(
                id=status_id,
                slug=task_status.slug,
                weight=task_status.weight,
                description=task_status.description,
            )
            for status_id, task_status in zip(status_ids, TaskStatusEnum)
        ]
