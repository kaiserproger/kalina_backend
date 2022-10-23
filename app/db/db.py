from app.imports import create_async_engine, AsyncSession
from app.domain.entities.base import Base


class Db:
    def __init__(self, url: str) -> None:
        self.engine = create_async_engine(url=url, echo=True)

    async def session(self):
        async with AsyncSession(bind=self.engine) as session_,\
                session_.begin():
            yield session_

    async def create_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
