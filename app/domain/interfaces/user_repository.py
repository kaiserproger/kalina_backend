from abc import ABC
from app.di.di_stubs import get_session_stub
from app.imports import AsyncSession
from app.domain.entities.user import User
from typing import Any, List

from fastapi import Depends


class UserRepositoryProto(ABC):
    def __init__(self,
                 session: AsyncSession = Depends(get_session_stub)) -> None:
        ...

    async def create(self, objekt: User):
        ...

    async def update(self, objekt: User, fields: dict[str, Any]):
        ...

    async def delete(self, id_: str) -> None:
        ...

    async def read_by_id(self, id_: str, no_joins: bool = False) -> User:
        ...

    async def read_multi(self, offset: int, limit: int) -> List[User]:
        ...
