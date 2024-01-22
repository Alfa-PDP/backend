from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UUID
from sqlalchemy.orm import Mapped, relationship

from database.models.declarative_base import BaseModel, Column
from database.models.mixins import IdMixin

if TYPE_CHECKING:
    from database.models.task import Task
    # from database.models.idp import Idp


class Tasknumber(BaseModel, IdMixin):
    __tablename__ = "task_number"

    idp_id: Mapped[UUID] = Column(
        ForeignKey("idp.id", ondelete="RESTRICT", onupdate="RESTRICT"), comment="ИПР связанный с задачей"
    )
    task_id: Mapped[UUID] = Column(
        ForeignKey("tasks.id", ondelete="RESTRICT", onupdate="RESTRICT"), comment="Порядковый номер в списке задач"
    )

    tasks: Mapped[list["Task"]] = relationship(back_populates="list_of_tasks")

    def __repr__(self) -> str:
        return f"Tasknumber({self.id}, {self.idp_id}, {self.task_id})"
