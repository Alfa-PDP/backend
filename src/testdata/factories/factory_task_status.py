from app.schemas.task_status import StatusSlugEnum
from database.models.status import Status
from testdata.factories.common_data import status_ids
from testdata.factories.factory_base import BaseSQLAlchemyFactory


class TaskStatusFactory(BaseSQLAlchemyFactory[Status]):
    @classmethod
    def build_all(cls) -> list[Status]:
        return [
            cls.build(id=status_id, slug=status_slug.value, weight=status_slug.weight)  # noqa
            for status_id, status_slug in zip(status_ids, StatusSlugEnum)
        ]
