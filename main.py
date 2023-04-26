from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.cabinet import cabinet_router
from src.api.auth import common_router
from src.api.revision import revision_router
from src.api.template import template_router
from src.auth.auth import AdminTokenAuthDecoder, TokenAuthDecoder,\
    TokenAuthEncoder, TokenInteractor
from src.core.settings import Settings
from src.di.di_stubs import get_redis_stub, get_session_stub, user_stub
from src.domain.entities.user import User
from src.domain.interfaces.admin_token_decoder import AdminTokenAuthDecoderProto
from src.domain.interfaces.cabinet_service import CabinetServiceProto
from src.domain.interfaces.form_repository import FormRepositoryProto
from src.domain.interfaces.form_service import FormServiceProto
from src.domain.interfaces.revision_repository import RevisionRepositoryProto
from src.domain.interfaces.revision_service import RevisionServiceProto
from src.domain.interfaces.token_auth_decoder import TokenAuthDecoderProto
from src.domain.interfaces.token_auth_encoder import TokenAuthEncoderProto
from src.domain.interfaces.token_interactor import TokenInteractorProto
from src.domain.interfaces.user_repository import UserRepositoryProto
from src.domain.interfaces.user_service import UserServiceProto
from src.exceptions.already_taken import AlreadyTakenException
from src.exceptions.handlers import alchemy_handler, already_taken_handler,\
    invalid_code_handler,\
    invalid_token_handler, invalid_value_handler, not_found_handler
from src.exceptions.invalid_code import InvalidCodeException
from src.exceptions.invalid_token import InvalidTokenException
from src.exceptions.not_found import NotFoundException
from src.db.db import Db, RedisConnector
from sqlalchemy.exc import SQLAlchemyError
from src.di.di import extract_user, get_form_service, get_user_repository,\
    get_cabinet_service,\
    get_form_repository, get_revision_repository, get_revision_service,\
    get_user_service


config = Settings()  # type: ignore

src = FastAPI()
db = Db(config.db_url)
redis_connector = RedisConnector(config.redis_url)

src.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@src.on_event("startup")
async def initialize():
    await db.create_all()


@src.on_event("shutdown")
async def shutdown():
    await db.engine.dispose()


# exception handlers
src.add_exception_handler(NotFoundException, not_found_handler)
src.add_exception_handler(SQLAlchemyError, alchemy_handler)
src.add_exception_handler(InvalidTokenException, invalid_token_handler)
src.add_exception_handler(AlreadyTakenException, already_taken_handler)
src.add_exception_handler(ValueError, invalid_value_handler)
src.add_exception_handler(AttributeError, invalid_value_handler)
src.add_exception_handler(InvalidCodeException, invalid_code_handler)

# routers
src.include_router(cabinet_router)
src.include_router(common_router)
src.include_router(revision_router)
src.include_router(template_router)

# actually, dependencies
src.dependency_overrides[get_session_stub] = db.session
src.dependency_overrides[get_redis_stub] = redis_connector.session
src.dependency_overrides[UserRepositoryProto] = get_user_repository
src.dependency_overrides[FormRepositoryProto] = get_form_repository
src.dependency_overrides[RevisionRepositoryProto] = get_revision_repository
src.dependency_overrides[RevisionServiceProto] = get_revision_service
src.dependency_overrides[CabinetServiceProto] = get_cabinet_service
src.dependency_overrides[UserServiceProto] = get_user_service
src.dependency_overrides[FormServiceProto] = get_form_service
src.dependency_overrides[TokenAuthDecoderProto] = TokenAuthDecoder
src.dependency_overrides[TokenAuthEncoderProto] = TokenAuthEncoder
src.dependency_overrides[AdminTokenAuthDecoderProto] = AdminTokenAuthDecoder
src.dependency_overrides[TokenInteractorProto] = TokenInteractor
src.dependency_overrides[user_stub] = extract_user
