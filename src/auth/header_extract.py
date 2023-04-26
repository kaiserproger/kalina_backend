from fastapi import Header

from src.exceptions.invalid_token import InvalidTokenException


class HeaderTokenExtractor:
    def __init__(self, authorization: str = Header()) -> None:
        self.value = authorization

    async def __call__(self) -> str:
        v = self.value.lower()
        if 'bearer' not in v:
            raise InvalidTokenException()
        return self.value.split()[1]
