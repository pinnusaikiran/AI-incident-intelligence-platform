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

import pandas as pd
from src.inference.prediction import PredictionResult
from src.inference.artifacts import InferenceArtifacts

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

    prediction = int(artifacts.model.predict(transformed_df)[0])

    probability = float(artifacts.model.predict_proba(transformed_df)[0][1])

    return PredictionResult(prediction=prediction,probability=probability)