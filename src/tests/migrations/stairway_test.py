import pytest
from alembic.command import downgrade, upgrade
from alembic.config import Config
from alembic.script import Script, ScriptDirectory
from sqlalchemy import Engine


def get_revisions() -> list[Script]:
    config = Config("alembic.ini")
    revisions_dir = ScriptDirectory.from_config(config)
    revisions = list(revisions_dir.walk_revisions("base", "heads"))
    revisions.reverse()
    return revisions


@pytest.mark.parametrize("revision", get_revisions())
def test_migrations_stairway(monkeypatch: pytest.MonkeyPatch, revision: Script, single_use_database: Engine) -> None:
    monkeypatch.setenv("MIGRATION_TEST", "True")

    alembic_config = Config("alembic.ini")

    alembic_config.set_main_option("sqlalchemy.url", single_use_database.url.render_as_string(hide_password=False))

    upgrade(alembic_config, revision.revision)
    downgrade(alembic_config, revision.down_revision or "-1")  # type: ignore
    upgrade(alembic_config, revision.revision)

    monkeypatch.delenv("MIGRATION_TEST")
