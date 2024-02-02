from typing import TYPE_CHECKING

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from database.models.declarative_base import BaseModel, Column

if TYPE_CHECKING:
    from database.models.task import Task
    # from database.models.idp import Idp


class TaskNumber(BaseModel):
    __tablename__ = "task_number"

    idp_id: Mapped[UUID] = Column(
        ForeignKey("idp.id", name="task_in_idp", ondelete="RESTRICT",
                   onupdate="RESTRICT"),
        comment="ИПР связанный с задачей",
    )
    task_id: Mapped[UUID] = Column(
        ForeignKey("tasks.id", name="task_id_list", ondelete="RESTRICT",
                   onupdate="RESTRICT"),
        comment="Порядковый номер в списке задач",
    )

    tasks: Mapped[list["Task"]] = relationship(back_populates="list_of_tasks")

    def __repr__(self) -> str:
        return f"TaskNumber({self.idp_id}, {self.task_id})"
