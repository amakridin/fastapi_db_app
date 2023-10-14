from typing import Optional

from fastapi import Depends, Header, Request, Security
from fastapi.security import APIKeyHeader
from jwt import ExpiredSignatureError

from src.core.bots import BotManager
from src.core.exceptions import (
    MissingApiKeyException,
    InvalidApiKeyException,
    MissingTokenException,
    InvalidTokenException,
    ExpiredTokenException,
)
from src.core.model import JwtTokenModel
from src.core.users import UserManager
from src.infra.repositories.db.db_bot_repository import DBBotRepository
from src.infra.repositories.db.db_user_repository import DBUserRepository
from src.infra.repositories.db.exceptions import EntityNotFoundException
from src.utils.jwt_manager import JWTManager, JWTDecodeException


def validate_api_key(
    request: Request,
    x_api_key: Optional[str] = Security(
        APIKeyHeader(
            name="X-Api-Key",
            description="api key",
            auto_error=False,
            scheme_name="api-key",
        )
    ),
) -> None:
    if not x_api_key:
        raise MissingApiKeyException
    if x_api_key != request.app.settings.api_key:
        raise InvalidApiKeyException


async def validate_token(
    request: Request,
    token: Optional[str] = Security(
        APIKeyHeader(
            name="token",
            description="token",
            auto_error=False,
            scheme_name="token",
        )
    ),
) -> None:
    if not token:
        raise MissingTokenException
    token_manager = JWTManager(secret_ket=request.app.settings.jwt_secret_key)
    try:
        token_info = JwtTokenModel(**token_manager.decode(token))
    except ExpiredSignatureError:
        raise ExpiredTokenException
    except JWTDecodeException:
        raise InvalidTokenException
    request.state.token = token
    request.state.bot_id = token_info.bot_id


def db_user_repo_dependency(request: Request):
    return DBUserRepository(
        db_schema=request.app.settings.db_schema, engine=request.app.resources.engine
    )


def user_manager_dependency(request: Request):
    return UserManager(
        db_user_repository=DBUserRepository(
            db_schema=request.app.settings.db_schema,
            engine=request.app.resources.engine,
        )
    )


def db_bot_repo_dependency(request: Request):
    return DBBotRepository(
        db_schema=request.app.settings.db_schema, engine=request.app.resources.engine
    )


def bot_manager_dependency(request: Request):
    return BotManager(
        db_bot_repository=DBBotRepository(
            db_schema=request.app.settings.db_schema,
            engine=request.app.resources.engine,
        ),
        jwt_manager=JWTManager(
            secret_key=request.app.settings.jwt_secret_key,
            ttl=0,
        ),
        schema_prefix=request.app.settings.bot_schema_prefix,
    )
