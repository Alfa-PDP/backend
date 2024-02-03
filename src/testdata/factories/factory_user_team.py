from database.models.user_team import UserTeam
from testdata.factories.common_data import team_ids, user_ids
from testdata.factories.factory_base import BaseSQLAlchemyFactory


class UserTeamFactory(BaseSQLAlchemyFactory[UserTeam]):
    @classmethod
    def build_all(cls) -> list[UserTeam]:
        factor = int(len(user_ids) / 2)

        return [cls.build(user_id=user_id, team_id=team_id) for user_id, team_id in zip(user_ids, team_ids * factor)]
