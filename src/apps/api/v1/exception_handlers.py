import logging
import re
from dataclasses import Field
from typing import Optional, Union

from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.core.exceptions import DomainException

logger = logging.getLogger(__name__)


class ErrorResponseModel(BaseModel):
    code: str
    details: Optional[Union[dict, str, list]] = None


async def internal_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception(exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponseModel(code="INTERNAL").dict(),
    )


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    logger.exception(exc)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=ErrorResponseModel(code="VALIDATION", details=exc.errors()).dict(),
    )


async def domain_exception_handler(request: Request, exc: DomainException):
    logger.exception(exc)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=ErrorResponseModel(code=str(exc), details=exc.details).dict(),
    )
