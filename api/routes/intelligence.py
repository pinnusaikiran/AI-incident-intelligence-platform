"""
Incident Intelligence endpoint.
"""

from fastapi import APIRouter, Depends

from api.schemas.prediction import PredictionRequest
from src.services.incident_intelligence_service import (
    IncidentIntelligenceService,
)

from api.dependencies import (
    get_prediction_service,
)

from rag.rag_service import RAGService


router = APIRouter(
    prefix="/intelligence",
    tags=["Incident Intelligence"],
)


rag_service = RAGService()


def get_intelligence_service(
    prediction_service=Depends(
        get_prediction_service
    ),
):

    return IncidentIntelligenceService(
        prediction_service=prediction_service,
        rag_service=rag_service,
    )


@router.post("/analyze")
def analyze_incident(
    request: PredictionRequest,
    question: str,
    service: IncidentIntelligenceService = Depends(
        get_intelligence_service
    ),
):

    return service.analyze(
        request=request,
        question=question,
    )