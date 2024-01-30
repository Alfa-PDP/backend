from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped

from database.models.declarative_base import BaseModel, Column
from database.models.mixins import IdMixin, TsMixinCreated, TsMixinUpdated


class User(BaseModel, IdMixin, TsMixinCreated, TsMixinUpdated):
    __tablename__ = "users"

    name: Mapped[str] = Column(String(50), nullable=False, comment="Имя пользователя")
    family_name: Mapped[str] = Column(String(50), nullable=False, comment="Фамилия пользователя")
    middle_name: Mapped[str] = Column(String(50), nullable=False, comment="Отчество пользователя")
    position: Mapped[str] = Column(String(100), nullable=False, comment="Должность пользователя")
    avatar: Mapped[str] = Column(Text, nullable=True, comment="Аватар пользователя")

    def __repr__(self) -> str:
        return f"User({self.id}, {self.name}, {self.family_name}, {self.position})"
