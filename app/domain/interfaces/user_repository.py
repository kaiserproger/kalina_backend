from abc import ABC, abstractmethod
from app.di.di_stubs import get_session_stub
from app.imports import AsyncSession
from app.domain.entities.user import User
from typing import List

from fastapi import Depends


class UserRepositoryProto(ABC):

    @abstractmethod
    def __init__(self,
                 session: AsyncSession = Depends(get_session_stub)) -> None:
        ...

    @abstractmethod
    async def create(self, objekt: User):
        ...

    @abstractmethod
    async def update(self, objekt: User):
        ...

    @abstractmethod
    async def delete(self, id_: str) -> None:
        ...

    @abstractmethod
    async def read_by_id(self, id_: str, no_joins: bool = False) -> User:
        ...

    @abstractmethod
    async def read_multi(self, offset: int, limit: int) -> List[User]:
        ...
