from abc import ABC, abstractmethod
from typing import Any, List
from uuid import UUID

from src.domain.entities.form import Form


class FormRepositoryProto(ABC):
    @abstractmethod
    async def create_form(self, form: Form):
        ...

    @abstractmethod
    async def update_form(self, objekt: Form, fields: dict[str, Any]):
        ...

    @abstractmethod
    async def delete_form(self, id_: UUID) -> None:
        ...

    @abstractmethod
    async def get_form_by_id(self, id_: UUID) -> Form:
        ...

    @abstractmethod
    async def get_all_forms(self, offset: int, limit: int) -> List[Form]:
        ...

    @abstractmethod
    async def get_template_forms(self) -> List[Form]:
        ...

    @abstractmethod
    async def create_form_from_template(self, template: Form) -> Form:
        ...
