from sqlalchemy import String
from sqlalchemy.orm import Mapped

from database.models.declarative_base import BaseModel, Column
from database.models.mixins import IdMixin


class Type(BaseModel, IdMixin):
    __tablename__ = "task_type"

    name: Mapped[str] = Column(String(20), nullable=False, comment="Тип задачи")

    def __repr__(self) -> str:
        return f"Type({self.id}, {self.name})"
