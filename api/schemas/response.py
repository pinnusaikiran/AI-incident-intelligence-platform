from pydantic import BaseModel, ConfigDict


class FeatureContributionResponse(BaseModel):
    """
    SHAP contribution of a single feature.
    """
    model_config = ConfigDict(from_attributes=True)

    feature: str
    impact: float


class ExplanationResponse(BaseModel):
    """
    SHAP explanation returned by the API.
    """
    model_config = ConfigDict(from_attributes=True)

    base_value: float
    feature_contributions: list[FeatureContributionResponse]


class PredictionInfoResponse(BaseModel):
    """
    Prediction information returned by the API.
    """
    model_config = ConfigDict(from_attributes=True)

    prediction_class: int
    prediction_label: str
    probability: float


class ModelInfoResponse(BaseModel):
    """
    Model information returned by the API.
    """
    model_config = ConfigDict(from_attributes=True)

    name: str
    version: str


class PredictionResponse(BaseModel):
    """
    Complete prediction response.
    """
    model_config = ConfigDict(from_attributes=True)

    prediction: PredictionInfoResponse
    explanation: ExplanationResponse
    model: ModelInfoResponse