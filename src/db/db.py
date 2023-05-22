from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from redis.asyncio import from_url


class Db:
    def __init__(self, url: str) -> None:
        self.engine = create_async_engine(url=url, echo=True)

    async def session(self):
        async with AsyncSession(bind=self.engine) as session_,\
                session_.begin():
            yield session_


class RedisConnector:
    def __init__(self, url: str) -> None:
        self.redis_client = from_url(url)

    async def session(self):
        async with self.redis_client.pipeline(transaction=True) as tx:
            yield tx

    async def dispose(self):
        await self.redis_client.close(close_connection_pool=True)
