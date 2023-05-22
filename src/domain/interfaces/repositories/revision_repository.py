from abc import ABC, abstractmethod
from typing import List, Any
from uuid import UUID

from src.domain.entities.revision import Revision


class RevisionRepositoryProto(ABC):
    @abstractmethod
    async def create_revision(self, revision: Revision):
        ...

    @abstractmethod
    async def update_revision(self, objekt: Revision, fields: dict[str, Any]):
        ...

    @abstractmethod
    async def delete_revision(self, id_: UUID) -> None:
        ...

    @abstractmethod
    async def get_revision_by_id(self, id_: UUID) -> Revision:
        ...

    @abstractmethod
    async def get_all_revisions(
        self,
        offset: int,
        limit: int
    ) -> List[Revision]:
        ...

    @abstractmethod
    async def get_available_revisions(
        self,
        offset: int = 0,
        limit: int = 0
    ) -> List[Revision]:
        ...
