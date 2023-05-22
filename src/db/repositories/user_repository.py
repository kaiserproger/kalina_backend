from typing import cast
from uuid import UUID

from sqlalchemy import update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.user import User
from domain.interfaces.repositories.user_repository import UserRepositoryProto
from src.exceptions.not_found import NotFoundException


class UserRepository(UserRepositoryProto):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_user(self, objekt: User):
        self.session.add(objekt)
        await self.session.flush()
        return objekt.phone

    async def update_user(self, objekt: User):
        statement = (update(User).
                     where(User.phone == objekt.phone).
                     values({}))
        await self.session.execute(statement)

    async def delete_user(self, id_: str) -> None:
        statement = delete(User).where(User.phone == id_)
        await self.session.execute(statement)

    async def get_user_by_phone(self, phone: str) -> User:
        user_query = select(User).where(User.phone == phone)
        user = (await self.session.execute(user_query)).scalar_one_or_none()
        if user is None:
            raise NotFoundException()
        return user

    async def get_all_users(self, offset: int, limit: int) -> list[User]:
        user_query = select(User).offset(offset).limit(limit)
        users = (await self.session.execute(user_query)).scalars().all()
        return cast(list[User], users)

    async def get_user_by_id(self, id: UUID):
        ...
