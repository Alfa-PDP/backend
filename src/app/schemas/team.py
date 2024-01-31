from uuid import UUID

from pydantic import BaseModel, ConfigDict  # noqa


class TeamSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    team_name: str
    leader_id: UUID
