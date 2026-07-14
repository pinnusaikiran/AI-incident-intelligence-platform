"""
Prediction endpoints.
"""

from fastapi import APIRouter,Depends

from api.dependencies import get_artifacts
from api.schemas import PredictionRequest,PredictionResponse

from src.inference.artifacts import InferenceArtifacts
from src.inference.validator import validate_request
from src.inference.predictor import predict
from src.inference.explainer import generate_explanation
from src.inference.response_builder import build_response

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
    artifacts: InferenceArtifacts=Depends(get_artifacts)
):
    """
    Predict whether an IT incident will breach its SLA.
    """
    
    request_data=request.model_dump()

    validate_df=validate_request(
        request_data=request_data,
        metadata=artifacts.metadata
        )
    
    transformed_df=artifacts.pipeline.transform(validate_df)
    prediction=predict(transformed_df=transformed_df,artifacts=artifacts)
    explanation=generate_explanation(transformed_df=transformed_df,artifacts=artifacts)
    response=build_response(
        prediction=prediction,
        explanation=explanation,
        metadata=artifacts.metadata
        )

    
    return PredictionResponse.model_validate(
        response,
        from_attributes=True
    )

    