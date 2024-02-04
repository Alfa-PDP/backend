import asyncio

from sqlalchemy.exc import IntegrityError

from testdata import factories
from testdata.factories.factory_base import BaseSQLAlchemyFactory

FACTORIES = [
    factories.UserFactory,
    factories.TeamFactory,
    factories.UserTeamFactory,
    factories.TaskStatusFactory,
    factories.IDPFactory,
    factories.TaskFactory,
    factories.TaskTypeFactory,
    factories.TaskImportanceFactory,
    factories.TaskCommentFactory,
    factories.GoalFactory,
]


async def main() -> None:
    for factory in FACTORIES:
        await _generate_data(factory)


async def _generate_data(factory: type[BaseSQLAlchemyFactory]) -> None:
    try:
        data = factory.build_all()
        await factory.add_all(data)
    except IntegrityError as err:
        print(err)


if __name__ == "__main__":
    asyncio.run(main())
