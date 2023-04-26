from uuid import UUID
from src.domain.entities.revision import Revision
from src.domain.interfaces.revision_repository import RevisionRepositoryProto
from src.exceptions.not_found import NotFoundException
from src.imports import AsyncSession, update, delete, select
from typing import Any, List


class RevisionRepository(RevisionRepositoryProto):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, revision: Revision):
        self.session.add(revision)
        await self.session.flush()

    async def update(self, objekt: Revision, fields: dict[str, Any]):
        statement = update(Revision).where(Revision.id ==
                                           objekt.id).values(**fields)
        await self.session.execute(statement)

    async def delete(self, id_: UUID) -> None:
        statement = delete(Revision).where(Revision.id == id_)
        await self.session.execute(statement)

    async def read_by_id(self, id_: UUID) -> Revision:
        revision = await self.session.get(Revision, id_)
        if revision is None:
            raise NotFoundException()
        return revision

    async def read_multi(self, offset: int, limit: int) -> List[Revision]:
        return (await self.session.execute(select(Revision).offset(offset).
                limit(limit))).scalars().all()

    async def read_available(self, offset: int = 0,
                             limit: int = 0) -> List[Revision]:
        return (await self.session.
                execute(select(Revision).
                        where(Revision.user_id is None).
                        where(not Revision.completed).
                        offset(offset).limit(limit))).scalars().all()
