from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from src.schemas.form import FormDTO

from .form_repository import FormRepositoryProto
from fastapi import Depends
from src.schemas.task import TaskDTO


class FormServiceProto(ABC):

    @abstractmethod
    def __init__(self, form_repo: FormRepositoryProto = Depends()):
        ...

    @abstractmethod
    async def create_template(self, tasks: list[TaskDTO], name: str):
        ...

    @abstractmethod
    async def get_templates(self) -> List[FormDTO]:
        ...

    @abstractmethod
    async def get_template(self, template_id: UUID) -> FormDTO:
        ...
