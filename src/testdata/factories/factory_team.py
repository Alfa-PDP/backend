from database.models.team import Team
from testdata.factories.common_data import leader_ids, team_ids
from testdata.factories.factory_base import BaseSQLAlchemyFactory


class TeamFactory(BaseSQLAlchemyFactory[Team]):
    @classmethod
    def team_name(cls) -> str:
        return cls.__faker__.city_suffix()

    @classmethod
    def build_all(cls) -> list[Team]:
        return [cls.build(id=team_id, leader_id=leader_id) for team_id, leader_id in zip(team_ids, leader_ids)]
