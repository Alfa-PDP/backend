from sqlalchemy import UUID, ForeignKey, String
from sqlalchemy.orm import Mapped

from database.models.declarative_base import BaseModel, Column
from database.models.mixins import IdMixin, TsMixinCreated, TsMixinUpdated


class Goal(BaseModel, IdMixin, TsMixinCreated, TsMixinUpdated):
    __tablename__ = "goals"

    user_id: Mapped[UUID] = Column(
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE", name="user_fkey"),
        comment="Номер сотрудника",
    )
    goal_name: Mapped[str] = Column(String(500), nullable=False, comment="Цель развития")
    employee_side_plus: Mapped[str] = Column(String(500), nullable=False, comment="Сильные стороны")
    employee_side_minus: Mapped[str] = Column(String(500), nullable=False, comment="Зоны развития")

    def __repr__(self) -> str:
        return (
            f"Goal({self.id}, {self.user_id}, {self.goal_name}, "
            f"{self.employee_side_plus}, {self.employee_side_minus})"
        )
