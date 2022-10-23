from app.domain.interfaces.base_repository import BaseRepository
from app.exceptions.not_found import NotFoundException
from app.imports import AsyncSession, update, delete, select, noload
from app.domain.entities.user import User
from typing import Any, List


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)

    async def create(self, objekt: User):
        self.session.add(objekt)
        await self.session.flush()
        return objekt.phone

    async def update(self, objekt: User, fields: dict[str, Any]):
        statement = update(User).where()
        await self.session.execute(statement)

    async def delete(self, id_: str) -> None:
        statement = delete(User).where(User.phone == id_)
        await self.session.execute(statement)

    async def read_by_id(self, id_: str, no_joins: bool = False) -> User:
        user = (await self.session.execute(select(User).
                where(User.phone == id_)
                .options(noload(User.revision)))).scalar_one_or_none()
        if user is None:
            raise NotFoundException()
        return user

    async def read_multi(self, offset: int, limit: int) -> List[User]:
        return (await self.session.execute(select(User).offset(offset).
                limit(limit))).scalars().all()
