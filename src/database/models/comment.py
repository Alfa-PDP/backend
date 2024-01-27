from sqlalchemy import ForeignKey, String, UUID
from sqlalchemy.orm import Mapped, relationship

from database.models.declarative_base import BaseModel, Column
from database.models.mixins import IdMixin, TsMixinCreated, TsMixinUpdated


class Comment(BaseModel, IdMixin, TsMixinCreated, TsMixinUpdated):
    __tablename__ = "comments"

    user_id: Mapped[UUID] = Column(
        ForeignKey("users.id", name="user_comment", ondelete="RESTRICT", onupdate="RESTRICT"),
        comment="Комментарий от пользователя",
    )
    task_id: Mapped[UUID] = Column(
        ForeignKey("tasks.id", name="task_comment", ondelete="RESTRICT", onupdate="RESTRICT"),
        comment="Комментарий задачи",
    )
    text: Mapped[str] = Column(String(1000), nullable=False, comment="Текст комментария")

    def __repr__(self) -> str:
        return f"Comment({self.user_id}, {self.task_id}, {self.text})"
