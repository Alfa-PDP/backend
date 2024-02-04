from app.schemas.tasks import TaskImportanceEnum
from database.models.task_importance import Importance
from database.models.task_type import Type
from testdata.factories.common_data import task_importance_ids
from testdata.factories.factory_base import BaseSQLAlchemyFactory


class TaskImportanceFactory(BaseSQLAlchemyFactory[Importance]):
    @classmethod
    def build_all(cls) -> list[Type]:
        return [
            cls.build(
                id=importance_id,
                name=task_importance.name,
            )
            for importance_id, task_importance in zip(task_importance_ids, TaskImportanceEnum)
        ]
