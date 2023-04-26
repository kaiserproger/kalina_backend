from .base import Base
from .task import Task
from src.imports import Column, ForeignKey, UUID, relationship, Boolean, String
from uuid import uuid4


class Form(Base):
    __tablename__ = "Form"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String)
    revision_id = Column(ForeignKey("Revision.id"),
                         nullable=True)  # type: ignore
    tasks: list[Task] = relationship(Task,
                                     cascade="all, delete-orphan")  # type: ignore
    is_template = Column(Boolean, default=False)
