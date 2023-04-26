from abc import ABC
from app.di.di_stubs import get_session_stub
from app.imports import AsyncSession
from app.domain.entities.revision import Revision
from typing import List, Any
from uuid import UUID
from fastapi import Depends


class RevisionRepositoryProto(ABC):
    def __init__(self,
                 session: AsyncSession = Depends(get_session_stub)) -> None:
        ...

    async def create(self, revision: Revision):
        ...

    async def update(self, objekt: Revision, fields: dict[str, Any]):
        ...

    async def delete(self, id_: UUID) -> None:
        ...

    async def read_by_id(self, id_: UUID) -> Revision:
        ...

    async def read_multi(self, offset: int, limit: int) -> List[Revision]:
        ...

    async def read_available(self, offset: int = 0,
                             limit: int = 0) -> List[Revision]:
        ...
