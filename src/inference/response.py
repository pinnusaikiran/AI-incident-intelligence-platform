from dataclasses import dataclass
from src.inference.explanation import ExplanationResult

@dataclass(frozen=True)
class PredictionInfo():
    """
    Prediction information returned to client
    """
    prediction_class:int
    prediction_label:str
    probability:float

@dataclass(frozen=True)
class ModelInfo:
    """
    Model metadata exposed through the API.
    """

    name: str
    version: str

@dataclass(frozen=True)
class APIResponse:
    """
    Complete inference response.
    """

    prediction: PredictionInfo
    explanation: ExplanationResult
    model: ModelInfo

