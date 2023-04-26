from abc import ABC, abstractmethod
from src.imports import AsyncSession
from src.domain.entities.form import Form
from typing import Any, List
from uuid import UUID
from src.di.di_stubs import get_session_stub

from fastapi import Depends


class FormRepositoryProto(ABC):
    def __init__(self, session: AsyncSession =
                 Depends(get_session_stub)) -> None:
        ...

    @abstractmethod
    async def create(self, form: Form):
        ...

    @abstractmethod
    async def update(self, objekt: Form, fields: dict[str, Any]):
        ...

    @abstractmethod
    async def delete(self, id_: UUID) -> None:
        ...

    @abstractmethod
    async def read_by_id(self, id_: UUID) -> Form:
        ...

    @abstractmethod
    async def read_multi(self, offset: int, limit: int) -> List[Form]:
        ...

    @abstractmethod
    async def get_templates(self) -> List[Form]:
        ...

    @abstractmethod
    async def create_from_template(self, template: Form) -> Form:
        ...
