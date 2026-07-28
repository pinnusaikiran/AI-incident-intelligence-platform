"""
FastAPI dependency providers.

This module contains reusable dependencies shared across API routes.
"""

from src.inference.artifacts import InferenceArtifacts
from src.inference.loader import load_artifacts
from src.services.prediction_service import PredictionService



def get_artifacts() -> InferenceArtifacts:
    """
    Return cached inference artifacts.

    Returns
    -------
    InferenceArtifacts
        Loaded model, preprocessing pipeline,
        SHAP explainer, and metadata.
    """ 
    return load_artifacts()

artifacts = get_artifacts()

prediction_service = PredictionService(
    artifacts=artifacts
)

def get_prediction_service() -> PredictionService:
    """
    Return the shared PredictionService instance.
    """
    return prediction_service
