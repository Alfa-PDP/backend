from typing import TYPE_CHECKING

from sqlalchemy import UUID, ForeignKey, String
from sqlalchemy.orm import Mapped, relationship

from database.models.declarative_base import BaseModel, Column
from database.models.mixins import IdMixin, TsMixinCreated, TsMixinUpdated

if TYPE_CHECKING:
    from database.models.user import User


class Team(BaseModel, IdMixin, TsMixinCreated, TsMixinUpdated):
    __tablename__ = "teams"

    name: Mapped[str] = Column(String(100), nullable=False, comment="Наименование команды")
    leader: Mapped[UUID] = Column(
        ForeignKey("users.id", ondelete="RESTRICT", onupdate="RESTRICT", name="teams_user_id_fkey"),
        comment="Порядковый номер сотрудника в списке команды, который назначен руководителем команды",
    )

    members: Mapped[list["User"]] = relationship(back_populates="team")

    def __repr__(self) -> str:
        return f"Team({self.id}, {self.name}, {self.leader})"
