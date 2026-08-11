"""
Global exception handlers.
"""

import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register all custom exception handlers.
    """

    @app.exception_handler(ValueError)
    async def value_error_handler(
        request: Request,
        exc: ValueError,
    ) -> JSONResponse:
        """
        Handle application validation errors.
        """
        logger.warning(
            "ValueError while processing %s %s : %s",
            request.method,
            request.url.path,
            exc,
        )

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "error": {
                    "type": "ValueError",
                    "message": str(exc),
                },
            },
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request,
        exc: StarletteHTTPException,
    ) -> JSONResponse:
        """
        Handle FastAPI/Starlette HTTP exceptions.
        """
        logger.warning(
            "HTTPException while processing %s %s : %s",
            request.method,
            request.url.path,
            exc.detail,
        )

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "type": "HTTPException",
                    "message": exc.detail,
                },
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        """
        Handle request body/query/path validation errors.
        """
        logger.warning(
            "RequestValidationError while processing %s %s",
            request.method,
            request.url.path,
        )

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                "success": False,
                "error": {
                    "type": "RequestValidationError",
                    "message": "Invalid request body or parameters.",
                    "details": exc.errors(),
                },
            },
        )

    @app.exception_handler(FileNotFoundError)
    async def file_not_found_handler(
        request: Request,
        exc: FileNotFoundError,
    ) -> JSONResponse:
        """
        Handle missing artifact or file errors.
        """
        logger.error(
            "FileNotFoundError while processing %s %s : %s",
            request.method,
            request.url.path,
            exc,
        )

        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "error": {
                    "type": "FileNotFoundError",
                    "message": str(exc),
                },
            },
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        """
        Handle all unexpected exceptions.
        """
        logger.exception(
            "Unhandled exception while processing %s %s",
            request.method,
            request.url.path,
        )

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": {
                    "type": "InternalServerError",
                    "message": "An unexpected error occurred.",
                },
            },
        )