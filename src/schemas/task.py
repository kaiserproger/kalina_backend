from pydantic import BaseModel

from src.schemas.answer import AnswerDto
from src.domain.entities.enums import TaskTypeEnum


class TaskDto(BaseModel):
    task_content: str
    task_type: TaskTypeEnum
    answers: list[AnswerDto]

    class Config:
        orm_mode = True
