from uuid import UUID
from typing import Any, List, cast

from sqlalchemy import update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.revision import Revision
from src.domain.interfaces.repositories.\
    revision_repository import RevisionRepositoryProto
from src.exceptions.not_found import NotFoundException


class RevisionRepository(RevisionRepositoryProto):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_revision(self, revision: Revision):
        self.session.add(revision)
        await self.session.flush()

    async def update_revision(self, objekt: Revision, fields: dict[str, Any]):
        statement = update(Revision).where(
            Revision.id == objekt.id
        ).values(**fields)
        await self.session.execute(statement)

    async def delete_revision(self, id_: UUID) -> None:
        statement = delete(Revision).where(Revision.id == id_)
        await self.session.execute(statement)

    async def get_revision_by_id(self, id_: UUID) -> Revision:
        revision = await self.session.get(Revision, id_)
        if revision is None:
            raise NotFoundException()
        return revision

    async def get_all_revisions(
        self,
        offset: int,
        limit: int
    ) -> List[Revision]:
        query = select(Revision).offset(offset).limit(limit)
        revisions = (await self.session.execute(query)).scalars().all()
        return cast(list[Revision], revisions)

    async def get_available_revisions(
        self,
        offset: int = 0,
        limit: int = 0
    ) -> List[Revision]:
        query = select(Revision).where(
            Revision.user_id.is_(None)
        ).offset(offset).limit(limit)
        revisions = (await self.session.execute(query)).scalars().all()
        return cast(list[Revision], revisions)
