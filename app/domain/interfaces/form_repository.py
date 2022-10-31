from abc import ABC
from app.imports import AsyncSession
from app.domain.entities.form import Form
from typing import Any, List
from uuid import UUID
from app.di.di_stubs import get_session_stub

from fastapi import Depends


class FormRepositoryProto(ABC):
    def __init__(self, session: AsyncSession =
                 Depends(get_session_stub)) -> None:
        ...

    async def create(self, form: Form):
        ...

    async def update(self, objekt: Form, fields: dict[str, Any]):
        ...

    async def delete(self, id_: UUID) -> None:
        ...

    async def read_by_id(self, id_: UUID) -> Form:
        ...

    async def read_multi(self, offset: int, limit: int) -> List[Form]:
        ...

    async def get_templates(self) -> List[Form]:
        ...

    async def create_from_template(self, template: Form) -> Form:
        ...
