from api.routes.health import router as health_router
from api.routes.prediction import router as prediction_router
from api.routes.assistant import router as assistant_router
from api.routes.intelligence import router as intelligence_router


__all__ = [
    "health_router",
    "prediction_router",
    "assistant_router",
    "intelligence_router",
]