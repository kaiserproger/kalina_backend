from datetime import datetime
from typing import Any
from uuid import UUID

from src.domain.entities.revision import Revision
from src.domain.entities.user import User
from domain.interfaces.repositories.form_repository import FormRepositoryProto
from domain.interfaces.repositories.\
    revision_repository import RevisionRepositoryProto
from domain.interfaces.services.revision_service import RevisionServiceProto
from domain.interfaces.repositories.user_repository import UserRepositoryProto
from src.schemas.form import FormDto
from src.schemas.revision import RevisionDto
from src.exceptions.already_taken import AlreadyTakenException
from src.exceptions.not_found import NotFoundException


class RevisionService(RevisionServiceProto):
    def __init__(self, revision_repo: RevisionRepositoryProto,
                 form_repo: FormRepositoryProto,
                 user_repo: UserRepositoryProto) -> None:
        self.rev_repo = revision_repo
        self.form_repo = form_repo
        self.user_repo = user_repo

    async def create_revision(self, form_id: UUID, address: str,
                              expire: datetime) -> None:
        template = await self.form_repo.get_form_by_id(form_id)
        form = await self.form_repo.create_form_from_template(template)
        revision = Revision(shop_address=address,
                            expire_date=expire)  # type: ignore
        revision.form = form
        await self.rev_repo.create_revision(revision)

    async def get_user_revision(self, user: User) -> Revision:
        user_joined = await self.user_repo.get_user_by_phone(user.phone)
        revision = user_joined.active_revision
        if revision is None:
            raise NotFoundException()

        return revision

    async def get_available_revisions(self) -> list[RevisionDto]:
        revisions = await self.rev_repo.get_available_revisions()
        return list(map(lambda model: RevisionDto.from_orm(model), revisions))

    async def update_current_revision(self, user: User,
                                      fields: dict[str, Any]) -> None:
        revision = await self.get_user_revision(user)
        await self.rev_repo.update_revision(revision, fields)

    async def update_revision_form(self, user: User, form: FormDto):
        revision = await self.get_user_revision(user)
        await self.form_repo.update_form(revision.form, form.dict())

    async def complete_revision(self, user: User):
        revision = await self.get_user_revision(user)
        await self.rev_repo.update_revision(revision, {"completed": True})

    async def select_revision(self, user: User, revision_id: UUID):
        revision = await self.rev_repo.get_revision_by_id(revision_id)
        if revision.user_id is not None:
            raise AlreadyTakenException()
        user.active_revision = revision
        await self.user_repo.update_user(user)

    async def approve_revision(self, id_: UUID):
        revision = await self.rev_repo.get_revision_by_id(id_)
        await self.rev_repo.update_revision(revision, {"approved": True})
