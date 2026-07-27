"""
Global Exception handlers
"""
from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from fastapi import status

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
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "error": {
                    "type": "ValueError",
                    "message":str(exc)
                        }
            }
        )