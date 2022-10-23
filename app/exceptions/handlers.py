from fastapi import Request
from fastapi.responses import JSONResponse, PlainTextResponse
from .not_found import NotFoundException
from .invalid_token import InvalidTokenException
from .already_taken import AlreadyTakenException
from .invalid_code import InvalidCodeException
from sqlalchemy.exc import SQLAlchemyError
from traceback import format_exc, print_exc


async def not_found_handler(request: Request, exc: NotFoundException):
    return JSONResponse({"message": str(exc)}, 404)


async def alchemy_handler(request: Request, exc: SQLAlchemyError):
    print_exc()
    return JSONResponse({"message": "DB error."}, 500)


async def invalid_token_handler(request: Request, exc: InvalidTokenException):
    return JSONResponse({"message": str(exc)}, 400)


async def already_taken_handler(request: Request, exc: AlreadyTakenException):
    return JSONResponse({"message": "Revision has been taken."}, 400)


async def invalid_value_handler(request: Request, exc: ValueError):
    print_exc()
    return JSONResponse({"message": str(exc)}, 422)


async def invalid_code_handler(request: Request, exc: InvalidCodeException):
    return PlainTextResponse(content=str(exc), status_code=404)
