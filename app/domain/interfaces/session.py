from abc import ABC


class SessionProto(ABC):
    async def flush(self):
        ...
