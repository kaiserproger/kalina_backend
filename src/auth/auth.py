from typing import Any

from fastapi import Depends
from redis.asyncio.client import Pipeline

from src.auth.header_extract import HeaderTokenExtractor
from src.auth.jwt import JWTInteractor
from src.di.di_stubs import get_redis_stub
from src.domain.entities.user import User
from src.domain.interfaces.token_auth_decoder import TokenAuthDecoderProto
from src.domain.interfaces.token_auth_encoder import TokenAuthEncoderProto
from src.domain.interfaces.token_interactor import TokenInteractorProto
from domain.interfaces.repositories.user_repository import UserRepositoryProto
from domain.interfaces.services.user_service import UserServiceProto
from src.exceptions.invalid_token import InvalidTokenException
from src.exceptions.not_found import NotFoundException


class TokenInteractor(TokenInteractorProto):
    def __init__(self, extractor: HeaderTokenExtractor =
                 Depends(),
                 jwt_interactor: JWTInteractor = Depends()) -> None:
        self.extractor = extractor
        self.jwt_interactor = jwt_interactor

    async def validate(self) -> dict[str, Any]:
        token = await self.extractor()
        if not token:
            raise InvalidTokenException()
        return await self.jwt_interactor.decode_token(token)


class TokenAuthDecoder(TokenAuthDecoderProto):
    def __init__(self, interactor: TokenInteractorProto = Depends(),
                 user_repo: UserRepositoryProto = Depends()) -> None:
        self.user_repo = user_repo
        self.interactor = interactor

    async def __call__(self) -> User:
        payload = await self.interactor.validate()
        user = await self.user_repo.get_user_by_phone(payload["phone"])
        return user


class TokenAuthEncoder(TokenAuthEncoderProto):
    def __init__(self, interactor: JWTInteractor = Depends()) -> None:
        self.interactor = interactor

    async def __call__(self, **kwds: Any) -> str:
        return await self.interactor.encode_token(kwds)


class AdminTokenAuthDecoder:
    def __init__(self, interactor: TokenInteractorProto = Depends(),
                 user_repo: UserRepositoryProto =
                 Depends()) -> None:
        self.interactor = interactor
        self.user_repo = user_repo

    async def __call__(self) -> Any:
        payload = await self.interactor.validate()
        user = await self.user_repo.get_user_by_phone(payload["phone"])
        if not user.admin:
            raise InvalidTokenException()


class PhoneAuthInteractor:
    def __init__(
        self,
        user_service: UserServiceProto = Depends(),
        token_encoder: TokenAuthEncoderProto = Depends(),
        redis: Pipeline = Depends(get_redis_stub)
    ) -> None:
        self.redis = redis
        self.user_service = user_service
        self.token_encoder = token_encoder
        self.code = 4043

    async def add_entry(self, phone: str):
        # # UNTESTED !!!!!
        await self.redis.hmset(phone, {
            "code": self.code,
            "activated": False
        })
        # END UNTESTED
        return self.code

    async def confirm(self, phone: str, code: int) -> str:
        # UNTESTED !!!!!
        value: int = await self.redis.hget(phone, "code")
        extracted_code = value
        if code != extracted_code:
            raise ValueError("Code mismatch!")
        await self.redis.hdel(phone, "code")
        await self.redis.hdel(phone, "activated")
        # END UNTESTED
        user = await self.user_service.get_user_by_phone(phone)
        return await self.token_encoder(**{"phone": user.phone,
                                           "admin": user.admin})

    async def finish_register(self, phone: str, name: str):
        value: dict = await self.redis.hgetall(phone)
        if not value:
            raise NotFoundException("No registration present!")
        if not value.get("activated"):
            raise InvalidTokenException("You haven't finished registration!")
        user = await self.user_service.create_user(phone, name)
        return await self.token_encoder(
            phone=user.phone,
            admin=user.admin
        )
