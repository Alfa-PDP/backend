from sqlalchemy import UUID, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped

from database.models.declarative_base import BaseModel, Column
from database.models.mixins import TsMixinCreated, TsMixinUpdated


class UserTeam(BaseModel, TsMixinCreated, TsMixinUpdated):
    __tablename__ = "users_teams"
    __table_args__ = (PrimaryKeyConstraint("user_id", "team_id", name="users_teams_pkey"),)

    user_id: Mapped[UUID] = Column(
        ForeignKey("users.id", ondelete="RESTRICT", onupdate="RESTRICT", name="users_teams_user_id_fkey")
    )
    team_id: Mapped[UUID] = Column(
        ForeignKey("teams.id", ondelete="RESTRICT", onupdate="RESTRICT", name="users_teams_team_id_fkey")
    )

    def __repr__(self) -> str:
        return f"UserTeam({self.user_id}, {self.team_id})"
