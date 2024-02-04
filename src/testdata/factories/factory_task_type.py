from app.schemas.tasks import TaskTypeEnum
from database.models.task_type import Type
from testdata.factories.common_data import task_type_ids
from testdata.factories.factory_base import BaseSQLAlchemyFactory


class TaskTypeFactory(BaseSQLAlchemyFactory[Type]):
    @classmethod
    def build_all(cls) -> list[Type]:
        return [
            cls.build(
                id=type_id,
                name=task_type.name,
            )
            for type_id, task_type in zip(task_type_ids, TaskTypeEnum)
        ]
