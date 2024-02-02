from database.models.idp import Idp
from testdata.factories.common_data import idp_dates, idp_ids, user_ids
from testdata.factories.factory_base import BaseSQLAlchemyFactory


class IDPFactory(BaseSQLAlchemyFactory[Idp]):
    @classmethod
    def build_all(cls) -> list[Idp]:
        return [
            cls.build(
                id=idp_id,
                user_id=user_id,
                start_date=dates[0],
                end_date=dates[1],
                year=dates[2],
            )
            for idp_id, user_id, dates in zip(idp_ids, user_ids, idp_dates)
        ]
