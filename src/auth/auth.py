from typing import Any
from app.auth.header_extract import HeaderTokenExtractor
from app.auth.jwt import JWTInteractor
from app.di.di_stubs import get_redis_stub
from app.domain.entities.user import User
from app.domain.interfaces.token_auth_decoder import TokenAuthDecoderProto
from app.domain.interfaces.token_auth_encoder import TokenAuthEncoderProto
from app.domain.interfaces.token_interactor import TokenInteractorProto
from app.domain.interfaces.user_repository import UserRepositoryProto
from app.domain.interfaces.user_service import UserServiceProto
from app.exceptions.invalid_token import InvalidTokenException
from app.exceptions.not_found import NotFoundException
from app.imports import Pipeline
from fastapi import Depends


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

    async def __call__(self, **kwds: Any) -> User:
        payload = await self.interactor.validate()
        user = await self.user_repo.read_by_id(payload["phone"], no_joins=True)
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
        user = await self.user_repo.read_by_id(payload["phone"], no_joins=True)
        if not user.admin:
            raise InvalidTokenException()


class PhoneAuthInteractor:

    def __init__(self, user_service: UserServiceProto =
                 Depends(),
                 token_encoder: TokenAuthEncoderProto =
                 Depends(),
                 redis: Pipeline =
                 Depends(get_redis_stub)) -> None:
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
        value: dict = await self.redis.hgetall(phone)
        extracted_code: int = value["code"]
        if code != extracted_code:
            raise ValueError("Code mismatch!")
        await self.redis.hmset(phone, {
            "code": extracted_code,
            "activated": True
        })
        # END UNTESTED
        user = await self.user_service.read_by_id(phone, True)
        return await self.token_encoder(**{"phone": user.phone,
                                           "admin": user.admin})

    async def finish_register(self, phone: str, name: str):
        # UNTESTED !!!!!
        value: dict = await self.redis.hgetall(phone)
        if not value:
            raise NotFoundException("No registration present!")
        if not value.get("activated"):
            raise InvalidTokenException("You haven't finished registration!")
        # END UNTESTED
        user = await self.user_service.create_user(phone, name)
        return await self.token_encoder(**{"phone": user.phone,
                                           "admin": user.admin})
