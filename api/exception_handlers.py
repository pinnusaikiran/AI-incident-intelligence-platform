"""
Global Exception handlers
"""
from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse

def register_exception_handlers(app:FastAPI) -> None:
    """
    Registers all custom exception handlers
    """
    @app.exception_handler(ValueError)
    async def value_error_handler(
        request: Request,
        exc: ValueError
    ):
        return JSONResponse(
            status_code=422,
            content={
                "details":str(exc)
            }
        )