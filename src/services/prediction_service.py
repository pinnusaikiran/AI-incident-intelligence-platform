from api.schemas.prediction import PredictionRequest

from src.inference.artifacts import InferenceArtifacts
from src.inference.feature_preparer import FeaturePreparer
from src.inference.predictor import predict
from src.inference.explainer import generate_explanation
from src.inference.response_builder import build_response
from src.inference.response import APIResponse
class PredictionService:
    """
    Orchestrates the complete inference workflow
    """
    def __init__(self, artifacts: InferenceArtifacts):

        self.artifacts = artifacts

        self.feature_preparer = FeaturePreparer(artifacts.pipeline)

    def predict(self,request:PredictionRequest) -> APIResponse:
        """
        Execute the complete prediction workflow.
        """
        transformed_features=self.feature_preparer.prepare(request)
        prediction=predict(
            transformed_df=transformed_features,
            artifacts=self.artifacts
        )
        explanation=generate_explanation(
            artifacts=self.artifacts,
            transformed_df=transformed_features
        )
        response = build_response(
            prediction=prediction,
            explanation=explanation,
            metadata=self.artifacts.metadata
        )

        return response
        