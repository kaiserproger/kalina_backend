from pydantic import BaseModel
from app.domain.entities.enums import TaskTypeEnum


class TaskDTO(BaseModel):
    task_content: str
    task_type: TaskTypeEnum
    answer: list[str]

    class Config:
        orm_mode = True
