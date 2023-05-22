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
from src.domain.interfaces.\
    admin_token_decoder import AdminTokenAuthDecoderProto
from domain.interfaces.services.cabinet_service import CabinetServiceProto
from domain.interfaces.repositories.form_repository import FormRepositoryProto
from domain.interfaces.services.form_service import FormServiceProto
from domain.interfaces.repositories.\
    revision_repository import RevisionRepositoryProto
from domain.interfaces.services.revision_service import RevisionServiceProto
from src.domain.interfaces.token_auth_decoder import TokenAuthDecoderProto
from src.domain.interfaces.token_auth_encoder import TokenAuthEncoderProto
from src.domain.interfaces.token_interactor import TokenInteractorProto
from domain.interfaces.repositories.user_repository import UserRepositoryProto
from domain.interfaces.services.user_service import UserServiceProto
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

app = FastAPI()
db = Db(config.db_url)
redis_connector = RedisConnector(config.redis_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("shutdown")
async def shutdown():
    await db.engine.dispose()
    await redis_connector.dispose()


# exception handlers
app.add_exception_handler(NotFoundException, not_found_handler)
app.add_exception_handler(SQLAlchemyError, alchemy_handler)
app.add_exception_handler(InvalidTokenException, invalid_token_handler)
app.add_exception_handler(AlreadyTakenException, already_taken_handler)
app.add_exception_handler(ValueError, invalid_value_handler)
app.add_exception_handler(AttributeError, invalid_value_handler)
app.add_exception_handler(InvalidCodeException, invalid_code_handler)

# routers
app.include_router(cabinet_router)
app.include_router(common_router)
app.include_router(revision_router)
app.include_router(template_router)

# actually, dependencies
app.dependency_overrides[get_session_stub] = db.session
app.dependency_overrides[get_redis_stub] = redis_connector.session
app.dependency_overrides[UserRepositoryProto] = get_user_repository
app.dependency_overrides[FormRepositoryProto] = get_form_repository
app.dependency_overrides[RevisionRepositoryProto] = get_revision_repository
app.dependency_overrides[RevisionServiceProto] = get_revision_service
app.dependency_overrides[CabinetServiceProto] = get_cabinet_service
app.dependency_overrides[UserServiceProto] = get_user_service
app.dependency_overrides[FormServiceProto] = get_form_service
app.dependency_overrides[TokenAuthDecoderProto] = TokenAuthDecoder
app.dependency_overrides[TokenAuthEncoderProto] = TokenAuthEncoder
app.dependency_overrides[AdminTokenAuthDecoderProto] = AdminTokenAuthDecoder
app.dependency_overrides[TokenInteractorProto] = TokenInteractor
app.dependency_overrides[user_stub] = extract_user
