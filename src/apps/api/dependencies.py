from typing import Optional

from fastapi import Request, Security
from fastapi.security import APIKeyHeader

from src.core.bots import BotManager
from src.core.exceptions import (
    MissingApiKeyException,
    InvalidApiKeyException,
)
from src.core.users import UserManager
from src.infra.repositories.db.db_bot_repository import DBBotRepository
from src.infra.repositories.db.db_user_repository import DBUserRepository


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


def db_user_repo_dependency(request: Request, bot_id: str):
    return DBUserRepository(
        db_schema=f"{request.app.settings.bot_schema_prefix}{bot_id}",
        engine=request.app.resources.engine,
    )


def user_manager_dependency(request: Request, bot_id: str):
    return UserManager(
        db_user_repository=DBUserRepository(
            db_schema=f"{request.app.settings.bot_schema_prefix}{bot_id}",
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
        schema_prefix=request.app.settings.bot_schema_prefix,
    )
