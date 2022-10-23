from abc import ABC
from .form_repository import FormRepositoryProto
from .revision_repository import RevisionRepositoryProto
from .user_repository import UserRepositoryProto
from uuid import UUID
from datetime import datetime
from app.domain.entities.user import User
from app.domain.entities.revision import Revision
from app.schemas.revision import RevisionDTO
from app.schemas.form import FormDTO
from typing import Any
from fastapi import Depends


class RevisionServiceProto(ABC):
    def __init__(self, revision_repo: RevisionRepositoryProto = Depends(),
                 form_repo: FormRepositoryProto = Depends(),
                 user_repo: UserRepositoryProto = Depends()) -> None:
        ...

    async def create_revision(self, form_id: UUID, address: str,
                              expire: datetime) -> None:
        ...

    async def get_user_revision(self, user: User) -> Revision:
        ...

    async def get_available_revisions(self) -> list[RevisionDTO]:
        ...

    async def update_current_revision(self, user: User,
                                      fields: dict[str, Any]) -> None:
        ...

    async def update_revision_form(self, user: User, form: FormDTO):
        ...

    async def complete_revision(self, user: User):
        ...

    async def select_revision(self, user: User, revision_id: UUID):
        ...

    async def approve_revision(self, id_: UUID):
        ...
