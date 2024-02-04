from itertools import zip_longest
from uuid import UUID

from app.schemas.tasks import ImportanceType, TaskType
from database.models.task import Task
from testdata.factories.common_data import idp_ids, status_ids, task_dates, task_ids, task_importance_ids, task_type_ids
from testdata.factories.factory_base import BaseSQLAlchemyFactory


class TaskFactory(BaseSQLAlchemyFactory[Task]):
    @classmethod
    def name(cls) -> str:
        return cls.__faker__.job()

    @classmethod
    def description(cls) -> str:
        return cls.__faker__.bs()

    @classmethod
    def task_type(cls) -> str:
        return cls.__faker__.random.choice([task_type.value for task_type in TaskType])

    @classmethod
    def importance(cls) -> str:
        return cls.__faker__.random.choice([importance.value for importance in ImportanceType])

    @classmethod
    def status_id(cls) -> UUID:
        return cls.__faker__.random.choice(status_ids)

    @classmethod
    def task_type_id(cls) -> UUID:
        return cls.__faker__.random.choice(task_type_ids)

    @classmethod
    def importance_id(cls) -> UUID:
        return cls.__faker__.random.choice(task_importance_ids)

    @classmethod
    def build_all(cls) -> list[Task]:
        factor = int(len(task_ids) / 10)

        return [
            cls.build(
                id=task_id,
                idp_id=idp_id,
                start_time=dates[0],
                end_time=dates[1],
            )
            for task_id, idp_id, dates in zip_longest(
                task_ids,
                idp_ids * factor,
                task_dates * factor,
            )
        ]
