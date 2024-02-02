from uuid import UUID, uuid4

from database.models.comment import Comment
from testdata.factories.common_data import task_ids, user_ids
from testdata.factories.factory_base import BaseSQLAlchemyFactory


class TaskCommentFactory(BaseSQLAlchemyFactory[Comment]):
    @classmethod
    def id(cls) -> UUID:
        return uuid4()

    @classmethod
    def build_all(cls) -> list[Comment]:
        ids = [uuid4() for _ in range(60)]
        factor = int(len(ids) / 10)

        return [
            cls.build(
                id=comment_id,
                task_id=task_id,
                user_id=user_id,
            )
            for comment_id, task_id, user_id in zip(ids, task_ids * factor, user_ids * factor)
        ]
