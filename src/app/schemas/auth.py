from uuid import UUID

from pydantic import BaseModel


class AuthData(BaseModel):
    user_id: UUID
    team_id: UUID
    is_leader: bool
