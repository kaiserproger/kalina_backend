from abc import ABC, abstractmethod
from .form_repository import FormRepositoryProto
from .revision_repository import RevisionRepositoryProto
from .user_repository import UserRepositoryProto
from uuid import UUID
from datetime import datetime
from src.domain.entities.user import User
from src.domain.entities.revision import Revision
from src.schemas.revision import RevisionDTO
from src.schemas.form import FormDTO
from typing import Any
from fastapi import Depends


class RevisionServiceProto(ABC):

    @abstractmethod
    def __init__(self, revision_repo: RevisionRepositoryProto = Depends(),
                 form_repo: FormRepositoryProto = Depends(),
                 user_repo: UserRepositoryProto = Depends()) -> None:
        ...

    @abstractmethod
    async def create_revision(self, form_id: UUID, address: str,
                              expire: datetime) -> None:
        ...

    @abstractmethod
    async def get_user_revision(self, user: User) -> Revision:
        ...

    @abstractmethod
    async def get_available_revisions(self) -> list[RevisionDTO]:
        ...

    @abstractmethod
    async def update_current_revision(self, user: User,
                                      fields: dict[str, Any]) -> None:
        ...

    @abstractmethod
    async def update_revision_form(self, user: User, form: FormDTO):
        ...

    @abstractmethod
    async def complete_revision(self, user: User):
        ...

    @abstractmethod
    async def select_revision(self, user: User, revision_id: UUID):
        ...

    @abstractmethod
    async def srcrove_revision(self, id_: UUID):
        ...
