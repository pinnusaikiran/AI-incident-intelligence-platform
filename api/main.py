from fastapi import FastAPI

from api.routes import (
    health_router,
    prediction_router,
)
from api.exception_handlers import register_exception_handlers
from api.middleware.request_id import RequestIDMiddleware
from src.logging.logger import configure_logging
import logging


configure_logging()


logger = logging.getLogger(__name__)

logger.info("Logging configured.")

app = FastAPI(
    title="AI Incident Intelligence Platform API",
    description=(
        "REST API for predicting IT Incident SLA Breaches "
        "using a trained CatBoost machine learning model."
    ),
    version="1.0.0",
)
logger.info("Application startup completed.")

app.add_middleware(RequestIDMiddleware)
register_exception_handlers(app)


app.include_router(health_router)
app.include_router(prediction_router)


@app.get("/")
def home():
    """
    Root endpoint.
    """
    return {
        "message": "Welcome to AI Incident Intelligence Platform API"
    }