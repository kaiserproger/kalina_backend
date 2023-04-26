from datetime import datetime
from typing import Any
from uuid import UUID
from app.domain.entities.revision import Revision
from app.domain.entities.user import User
from app.domain.interfaces.form_repository import FormRepositoryProto
from app.domain.interfaces.revision_repository import RevisionRepositoryProto
from app.domain.interfaces.revision_service import RevisionServiceProto
from app.domain.interfaces.user_repository import UserRepositoryProto
from app.schemas.form import FormDTO
from app.schemas.revision import RevisionDTO
from app.exceptions.already_taken import AlreadyTakenException
from app.exceptions.not_found import NotFoundException


class RevisionService(RevisionServiceProto):
    def __init__(self, revision_repo: RevisionRepositoryProto,
                 form_repo: FormRepositoryProto,
                 user_repo: UserRepositoryProto) -> None:
        self.rev_repo = revision_repo
        self.form_repo = form_repo
        self.user_repo = user_repo

    async def create_revision(self, form_id: UUID, address: str,
                              expire: datetime) -> None:
        template = await self.form_repo.read_by_id(form_id)
        form = await self.form_repo.create_from_template(template)
        revision = Revision(shop_address=address,
                            expire_date=expire)  # type: ignore
        revision.form = form
        await self.rev_repo.create(revision)

    async def get_user_revision(self, user: User) -> Revision:
        user_joined = (await self.user_repo.
                       read_by_id(user.phone))  # type: ignore
        if user_joined.revision is None or user_joined.revision.id is None:
            raise NotFoundException()
        return user_joined.revision

    async def get_available_revisions(self) -> list[RevisionDTO]:
        revisions = await self.rev_repo.read_available()
        return list(map(lambda model: RevisionDTO.from_orm(model), revisions))

    async def update_current_revision(self, user: User,
                                      fields: dict[str, Any]) -> None:
        revision = await self.get_user_revision(user)
        await self.rev_repo.update(revision, fields)

    async def update_revision_form(self, user: User, form: FormDTO):
        revision = await self.get_user_revision(user)
        await self.form_repo.update(revision.form, form.dict())

    async def complete_revision(self, user: User):
        revision = await self.get_user_revision(user)
        await self.rev_repo.update(revision, {"completed": True})

    async def select_revision(self, user: User, revision_id: UUID):
        revision = await self.rev_repo.read_by_id(revision_id)
        if revision.user_id is not None:
            raise AlreadyTakenException()
        user.revision = revision
        await self.user_repo.update(user)

    async def approve_revision(self, id_: UUID):
        revision = await self.rev_repo.read_by_id(id_)
        await self.rev_repo.update(revision, {"approved": True})
