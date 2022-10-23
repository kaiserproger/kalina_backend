from app.domain.entities.enums import TaskTypeEnum
from .base import Base
from app.imports import Column, String, Enum, ARRAY, UUID, ForeignKey
from uuid import uuid4


class Task(Base):
    __tablename__ = "Task"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    form_id = Column(UUID(as_uuid=True), ForeignKey("Form.id"))  # type: ignore
    task_content = Column(String)
    task_type = Column(Enum(TaskTypeEnum))
    answers = Column(ARRAY(String, dimensions=1, zero_indexes=True))
