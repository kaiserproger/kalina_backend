from abc import ABC
from typing import Any, Generic, List, Type, TypeVar
from uuid import UUID
from app.domain.entities.base import Base
from app.imports import AsyncSession


ModelClass = TypeVar("ModelClass", bound=Base)  # type: ignore


class BaseRepository(ABC, Generic[ModelClass]):
    def __init__(self, session: AsyncSession, model_cls: Type[ModelClass])\
            -> None:
        self.session = session
        self.model_cls = model_cls

    async def create(self, objekt: ModelClass) -> UUID:
        raise NotImplementedError()

    async def update(self, objekt: ModelClass, fields: dict[str, Any]) -> None:
        raise NotImplementedError()

    async def delete(self, id_: UUID) -> bool:
        raise NotImplementedError()

    async def read_by_id(self, id_: UUID) -> ModelClass:
        raise NotImplementedError()

    async def read_multi(self, offset: int, limit: int) -> List[ModelClass]:
        raise NotImplementedError()
