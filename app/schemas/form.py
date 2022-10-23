from uuid import UUID
from pydantic import BaseModel
from .task import TaskDTO


class FormDTO(BaseModel):
    name: str
    revision_id: UUID
    tasks: list[TaskDTO]
    is_template: bool

    class Config:
        orm_mode = True
