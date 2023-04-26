from typing import Any
from jwt import encode, decode


class JWTInteractor:
    def __init__(self):
        self.secret = "f2cc6d52446cb2e27f7e8a9a2cca433ea211f36de8b067d84dbc30c6d83a5cc6"

    async def encode_token(self, payload: dict[str, Any]):
        return encode(payload, self.secret)

    async def decode_token(self, token: str):
        return decode(token, self.secret, ["HS256"])
