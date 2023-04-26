from src.imports import create_async_engine, AsyncSession
from src.domain.entities.base import Base
from redis.asyncio import from_url


class Db:
    def __init__(self, url: str) -> None:
        self.engine = create_async_engine(url=url, echo=True)

    async def session(self):
        async with AsyncSession(bind=self.engine) as session_,\
                session_.begin():
            yield session_

    async def create_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)  # type: ignore


class RedisConnector:
    def __init__(self, url: str) -> None:
        self.redis_client = from_url(url)

    async def session(self):
        async with self.redis_client.pipeline(transaction=True) as tx:
            yield tx
