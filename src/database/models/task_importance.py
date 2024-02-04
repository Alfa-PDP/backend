from sqlalchemy import String
from sqlalchemy.orm import Mapped

from database.models.declarative_base import BaseModel, Column
from database.models.mixins import IdMixin


class Importance(BaseModel, IdMixin):
    __tablename__ = "task_importance"

    name: Mapped[str] = Column(String(20), nullable=False, comment="Уровень значимости задачи")

    def __repr__(self) -> str:
        return f"Importance({self.id}, {self.name})"
