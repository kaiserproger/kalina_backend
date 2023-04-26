from src.domain.interfaces.user_repository import UserRepositoryProto
from src.exceptions.not_found import NotFoundException
from src.imports import AsyncSession, update, delete, select, noload
from src.domain.entities.user import User
from typing import Any, List


class UserRepository(UserRepositoryProto):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, objekt: User):
        self.session.add(objekt)
        await self.session.flush()
        return objekt.phone

    async def update(self, objekt: User):
        statement = (update(User).where(User.phone == objekt.phone).
                     values({}))  # TODO: Generate diff between old and new objekt
        await self.session.execute(statement)

    async def delete(self, id_: str) -> None:
        statement = delete(User).where(User.phone == id_)
        await self.session.execute(statement)

    async def read_by_id(self, id_: str, no_joins: bool = False) -> User:
        user_query = select(User).where(User.phone == id_)
        if no_joins:
            user_query = user_query.options(noload(User.revision))
        user = (await self.session.execute(user_query)).scalar_one_or_none()
        if user is None:
            raise NotFoundException()
        return user

    async def read_multi(self, offset: int, limit: int) -> List[User]:
        return (await self.session.execute(select(User).offset(offset).
                limit(limit))).scalars().all()
