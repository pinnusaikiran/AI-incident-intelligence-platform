"""
Prediction endpoints.
"""

from fastapi import APIRouter,Depends

from api.dependencies import get_prediction_service
from api.schemas import PredictionRequest,PredictionResponse

from src.services.prediction_service import PredictionService

router = APIRouter(
    prefix="/predict",
    tags=["Prediction"],
)


@router.post(
    "",
    response_model=PredictionResponse,
    summary="Predict SLA Breach"
)
def predict_incident(
    request: PredictionRequest,
    service: PredictionService = Depends(get_prediction_service)
):
    """
    Predict whether an IT incident will breach its SLA.
    """
    
    response = service.predict(request)

    return PredictionResponse.model_validate(
        response,
        from_attributes=True
    )

    