from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, relationship

from database.models.declarative_base import BaseModel, Column
from database.models.mixins import IdMixin, TsMixinCreated, TsMixinUpdated

if TYPE_CHECKING:
    from database.models.idp import Idp
    from database.models.task import Task


class User(BaseModel, IdMixin, TsMixinCreated, TsMixinUpdated):
    __tablename__ = "users"

    name: Mapped[str] = Column(String(50), nullable=False, comment="Имя пользователя")
    family_name: Mapped[str] = Column(String(50), nullable=False, comment="Фамилия пользователя")
    middle_name: Mapped[str] = Column(String(50), nullable=False, comment="Отчество пользователя")
    position: Mapped[str] = Column(String(100), nullable=False, comment="Должность пользователя")
    avatar: Mapped[str] = Column(Text, nullable=True, comment="Аватар пользователя")

    idp: Mapped["Idp"] = relationship()
    tasks: Mapped[list["Task"]] = relationship(secondary="join(Idp, Task, Idp.id == Task.idp_id)")

    def __repr__(self) -> str:
        return f"User({self.id}, {self.name}, {self.family_name}, {self.position})"
