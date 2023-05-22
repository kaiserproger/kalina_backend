from uuid import UUID

from pydantic import BaseModel

from src.schemas.task import TaskDto


class FormDto(BaseModel):
    name: str
    revision_id: UUID
    tasks: list[TaskDto]
    is_template: bool

    class Config:
        orm_mode = True
