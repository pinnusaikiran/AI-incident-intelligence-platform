from fastapi import FastAPI

from api.routes import (
    health_router,
    prediction_router,
    assistant_router,
    intelligence_router,
)

from api.exception_handlers import (
    register_exception_handlers,
)

from api.middleware.request_id import (
    RequestIDMiddleware,
)

from src.logging.logger import (
    configure_logging,
)

import logging


configure_logging()

logger = logging.getLogger(__name__)


app = FastAPI(
    title="AI Incident Intelligence Platform API",
    description=(
        "AI-powered IT Incident Intelligence Platform "
        "for SLA breach prediction, explainability, "
        "RAG and incident intelligence."
    ),
    version="2.0.0",
)


app.add_middleware(
    RequestIDMiddleware
)

register_exception_handlers(app)


app.include_router(
    health_router
)

app.include_router(
    prediction_router
)

app.include_router(
    assistant_router
)

app.include_router(
    intelligence_router
)


@app.get("/")
def home():

    return {
        "message": (
            "Welcome to AI Incident Intelligence Platform API"
        ),
        "version": "2.0.0",
    }