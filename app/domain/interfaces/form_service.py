from abc import ABC
from typing import List
from uuid import UUID

from app.schemas.form import FormDTO

from .form_repository import FormRepositoryProto
from fastapi import Depends
from app.schemas.task import TaskDTO


class FormServiceProto(ABC):
    def __init__(self, form_repo: FormRepositoryProto = Depends()):
        ...

    async def create_template(self, tasks: list[TaskDTO], name: str):
        ...

    async def get_templates(self) -> List[FormDTO]:
        ...

    async def get_template(self, template_id: UUID) -> FormDTO:
        ...
