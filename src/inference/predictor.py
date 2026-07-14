"""
Generate a prediction for the incoming request.

The request is validated, transformed using the
preprocessing pipeline, and passed to the trained
CatBoost model for prediction.

Returns
-------
PredictionResult
    Predicted class label and positive-class probability.
"""
from typing import Any
import pandas as pd
from src.inference.prediction import PredictionResult
from src.inference.artifacts import InferenceArtifacts
from src.inference.validator import validate_request



def predict(
    transformed_df: pd.DataFrame,
    artifacts: InferenceArtifacts,
) -> PredictionResult:
    """
    Generate a prediction for the incoming request.

    The request is validated, transformed using the preprocessing pipeline, and passed to the trained CatBoost model.

    Parameters
    ----------
    request_data : dict[str, Any]
        Incoming request payload.

    artifacts : InferenceArtifacts
        Loaded model artifacts required for inference.

    Returns
    -------
    PredictionResult
        Predicted class label and probability of the
        positive class (SLA Breach).
    """
    # df=validate_request(request_data=request_data,metadata=artifacts.metadata)
    # transformed_df = artifacts.pipeline.transform(df)
    prediction = int(artifacts.model.predict(transformed_df)[0])

    probability = float(artifacts.model.predict_proba(transformed_df)[0][1])

    return PredictionResult(prediction=prediction,probability=probability)