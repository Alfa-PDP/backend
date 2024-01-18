from sqlalchemy import Text
from sqlalchemy.orm import Mapped

from database.models.declarative_base import BaseModel, Column
from database.models.mixins import IdMixin, TsMixinCreated, TsMixinUpdated


class User(BaseModel, IdMixin, TsMixinCreated, TsMixinUpdated):
    """Data model for public.users db table."""

    __tablename__ = "users"

    name: Mapped[str] = Column(Text, nullable=False, comment="Имя пользователя")
    family_name: Mapped[str] = Column(Text, nullable=False, comment="Фамилия пользователя")
    surname: Mapped[str] = Column(Text, nullable=False, comment="Отчество пользователя")
    position: Mapped[str] = Column(Text, nullable=False, comment="Должность пользователя")
    role: Mapped[str] = Column(Text, nullable=False, comment="Роль пользователя")

    def __repr__(self) -> str:
        return f"User({self.id}, {self.name}, {self.family_name}, {self.role})"
