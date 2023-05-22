from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID
from datetime import datetime

from src.domain.entities.user import User
from src.domain.entities.revision import Revision
from src.schemas.revision import RevisionDto
from src.schemas.form import FormDto


class RevisionServiceProto(ABC):
    @abstractmethod
    async def create_revision(self, form_id: UUID, address: str,
                              expire: datetime) -> None:
        ...

    @abstractmethod
    async def get_user_revision(self, user: User) -> Revision:
        ...

    @abstractmethod
    async def get_available_revisions(self) -> list[RevisionDto]:
        ...

    @abstractmethod
    async def update_current_revision(self, user: User,
                                      fields: dict[str, Any]) -> None:
        ...

    @abstractmethod
    async def update_revision_form(self, user: User, form: FormDto):
        ...

    @abstractmethod
    async def complete_revision(self, user: User):
        ...

    @abstractmethod
    async def select_revision(self, user: User, revision_id: UUID):
        ...

    @abstractmethod
    async def approve_revision(self, id_: UUID):
        ...
