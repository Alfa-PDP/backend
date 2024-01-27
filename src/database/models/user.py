from typing import TYPE_CHECKING

from sqlalchemy import UUID, ForeignKey, String
from sqlalchemy.orm import Mapped, relationship

from database.models.declarative_base import BaseModel, Column
from database.models.mixins import IdMixin, TsMixinCreated, TsMixinUpdated

if TYPE_CHECKING:
    from database.models.team import Team


class User(BaseModel, IdMixin, TsMixinCreated, TsMixinUpdated):
    __tablename__ = "users"

    name: Mapped[str] = Column(String(50), nullable=False, comment="Имя сотрудника")
    family_name: Mapped[str] = Column(String(50), nullable=False, comment="Фамилия сотрудника")
    surname: Mapped[str] = Column(
        String(50),
        nullable=False,
        comment="Наименование должности / специальности в команде",
    )
    position: Mapped[str] = Column(String(100), nullable=False, comment="Должность сотрудника")
    role: Mapped[str] = Column(String(50), nullable=False, comment="Роль сотрудника")
    team_id: Mapped[UUID] = Column(
        ForeignKey("teams.id", ondelete="RESTRICT", onupdate="RESTRICT", name="users_team_id_fkey"),
        comment="Порядковый номер в списке команды",
    )

    team: Mapped["Team"] = relationship(back_populates="members")

    def __repr__(self) -> str:
        return f"User({self.id}, {self.name}, {self.family_name}, {self.role})"
