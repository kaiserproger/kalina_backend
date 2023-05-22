from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from src.schemas.form import FormDto
from src.schemas.task import TaskDto


class FormServiceProto(ABC):
    @abstractmethod
    async def create_template(self, tasks: list[TaskDto], name: str):
        ...

    @abstractmethod
    async def get_templates(self) -> List[FormDto]:
        ...

    @abstractmethod
    async def get_template(self, template_id: UUID) -> FormDto:
        ...
