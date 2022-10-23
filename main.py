from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.cabinet import cabinet_router
from app.api.common import common_router
from app.api.revision import revision_router
from app.api.template import template_router
from app.auth.auth import AdminTokenAuthDecoder, TokenAuthDecoder, TokenAuthEncoder, TokenInteractor
from app.di.di_stubs import get_session_stub
from app.domain.entities.user import User
from app.domain.interfaces.admin_token_decoder import AdminTokenAuthDecoderProto
from app.domain.interfaces.cabinet_service import CabinetServiceProto
from app.domain.interfaces.form_repository import FormRepositoryProto
from app.domain.interfaces.form_service import FormServiceProto
from app.domain.interfaces.revision_repository import RevisionRepositoryProto
from app.domain.interfaces.revision_service import RevisionServiceProto
from app.domain.interfaces.token_auth_decoder import TokenAuthDecoderProto
from app.domain.interfaces.token_auth_encoder import TokenAuthEncoderProto
from app.domain.interfaces.token_interactor import TokenInteractorProto
from app.domain.interfaces.user_repository import UserRepositoryProto
from app.domain.interfaces.user_service import UserServiceProto
from app.exceptions.already_taken import AlreadyTakenException
from app.exceptions.handlers import alchemy_handler, already_taken_handler, invalid_code_handler,\
    invalid_token_handler, invalid_value_handler, not_found_handler
from app.exceptions.invalid_code import InvalidCodeException
from app.exceptions.invalid_token import InvalidTokenException
from app.exceptions.not_found import NotFoundException
from app.db.db import Db
from sqlalchemy.exc import SQLAlchemyError
from app.di.di import extract_user, get_form_service, get_user_repository, get_cabinet_service,\
    get_form_repository, get_revision_repository, get_revision_service,\
    get_user_service


app = FastAPI()
db = Db("postgresql+asyncpg://postgres:postgres@localhost/main")

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def initialize():
    await db.create_all()


@app.on_event("shutdown")
async def shutdown():
    await db.engine.dispose()

app.add_exception_handler(NotFoundException, not_found_handler)
app.add_exception_handler(SQLAlchemyError, alchemy_handler)
app.add_exception_handler(InvalidTokenException, invalid_token_handler)
app.add_exception_handler(AlreadyTakenException, already_taken_handler)
app.add_exception_handler(ValueError, invalid_value_handler)
app.add_exception_handler(AttributeError, invalid_value_handler)
app.add_exception_handler(InvalidCodeException, invalid_code_handler)
app.include_router(cabinet_router)
app.include_router(common_router)
app.include_router(revision_router)
app.include_router(template_router)
app.dependency_overrides[get_session_stub] = db.session
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
app.dependency_overrides[User] = extract_user
