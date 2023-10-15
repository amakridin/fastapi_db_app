import logging

from functools import partial

import uvicorn
from aiopg.sa import create_engine
from fastapi import (
    Depends,
    FastAPI,
)
from fastapi.exceptions import RequestValidationError

from pydantic import BaseSettings, ValidationError
from starlette import status

from resources import Resources
from src.apps.api.dependencies import validate_api_key
from src.apps.api.v1.exception_handlers import (
    ErrorResponseModel,
    internal_exception_handler,
    request_validation_exception_handler,
    domain_exception_handler,
)
from src.core.exceptions import DomainException

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    port: int = 8001
    service_name: str = "user-service"
    api_key: str = "admin-api-key"
    jwt_secret_key = "access-secret-key"
    jwt_token_ttl = 0
    gateway_timeout_s: int = 2
    db_schema: str = "public"
    bot_schema_prefix: str = "bot_"
    dsn = "postgresql://postgres:postgres@localhost:35432/users"
    pg_min_pool_size: int = 5
    pg_max_pool_size: int = 20

    # class Config:
    #     env_file = "local.env"


def create_app(settings: Settings) -> FastAPI:
    # App
    app = FastAPI(
        title="user-service",
        version="v1",
        responses={
            status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseModel},
            status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponseModel},
        },
        exception_handlers={
            RequestValidationError: request_validation_exception_handler,
            DomainException: domain_exception_handler,
            ValidationError: request_validation_exception_handler,
            Exception: internal_exception_handler,
        },
    )
    app.settings = settings

    # Routing
    from src.apps.api.v1.views import ROUTERS

    for r in ROUTERS:
        app.include_router(r)

    # Events
    app.add_event_handler("startup", partial(on_startup, app, settings))
    app.add_event_handler("shutdown", partial(on_shutdown, app))

    return app


async def on_startup(app, settings):
    logger.info("Init resources")
    app.resources = await Resources.init_resources(settings)
    logger.info("Start web app")


async def on_shutdown(app):
    logger.info("Shutdown resources")
    app.resources.engine.close()
    logger.info("Stop web app")
