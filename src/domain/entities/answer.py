from uuid import UUID
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.entities.base import Base

if TYPE_CHECKING:
    from src.domain.entities.task import Task


class Answer(Base):
    __tablename__ = "answers"

    task_id: Mapped[UUID] = mapped_column(ForeignKey("Task.id"), init=False)
    task: Mapped["Task"] = relationship(back_populates="answers", init=False)
    content: Mapped[str]
