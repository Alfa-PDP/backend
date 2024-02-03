from database.models.goal import Goal
from testdata.factories.common_data import user_ids, goal_ids, goal_goal_name, goal_employee_side_plus, \
    goal_employee_side_minus
from testdata.factories.factory_base import BaseSQLAlchemyFactory


class GoalFactory(BaseSQLAlchemyFactory[Goal]):

    @classmethod
    def build_all(cls) -> list[Goal]:
        return [
            cls.build(
                id=goal_id,
                user_id=user_id,
                goal_name=goal_name,
                employee_side_plus=side_plus,
                employee_side_minus=side_minus,
            )
            for goal_id, user_id, goal_name, side_plus, side_minus in zip(
                goal_ids, user_ids, goal_goal_name, goal_employee_side_plus, goal_employee_side_minus
            )
        ]
