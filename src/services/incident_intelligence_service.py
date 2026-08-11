from api.schemas.prediction import PredictionRequest

from src.services.prediction_service import PredictionService

from rag.rag_service import RAGService


class IncidentIntelligenceService:
    """
    Orchestrates ML prediction, SHAP explanation,
    RAG retrieval, and LLM-generated operational guidance.
    """

    def __init__(
        self,
        prediction_service: PredictionService,
        rag_service: RAGService,
    ):
        self.prediction_service = prediction_service
        self.rag_service = rag_service

    @staticmethod
    def _build_risk_context(prediction_response) -> dict:
        """
        Build deterministic risk information for the LLM.

        The ML model is the source of truth for prediction.
        The LLM must not reinterpret the prediction.
        """

        prediction = prediction_response.prediction

        breach_probability = prediction.probability

        # CatBoost's default binary decision boundary
        # is 0.5 for the prediction class.
        threshold = 0.5

        distance_from_threshold = abs(
            breach_probability - threshold
        )

        if distance_from_threshold <= 0.05:
            risk_level = "Borderline"
        elif breach_probability >= threshold:
            risk_level = "High"
        else:
            risk_level = "Low"

        top_contributors = sorted(
            prediction_response.explanation.feature_contributions,
            key=lambda item: abs(item.impact),
            reverse=True,
        )[:5]

        return {
            "prediction_class": prediction.prediction_class,
            "prediction_label": prediction.prediction_label,
            "sla_breach_probability": breach_probability,
            "decision_threshold": threshold,
            "risk_level": risk_level,
            "top_shap_contributors": [
                {
                    "feature": item.feature,
                    "impact": item.impact,
                }
                for item in top_contributors
            ],
        }

    def analyze(
        self,
        request: PredictionRequest,
        question: str,
    ):
        """
        Execute the complete incident intelligence workflow.
        """

        # --------------------------------------------------
        # 1. ML prediction + SHAP
        # --------------------------------------------------

        prediction_response = self.prediction_service.predict(
            request
        )

        # --------------------------------------------------
        # 2. Build deterministic ML context
        # --------------------------------------------------

        risk_context = self._build_risk_context(
            prediction_response
        )

        # --------------------------------------------------
        # 3. RAG + LLM
        # --------------------------------------------------

        rag_response = self.rag_service.ask(
            question=question,
            incident_context=risk_context,
        )

        # --------------------------------------------------
        # 4. Return combined result
        # --------------------------------------------------

        return {
            "prediction": prediction_response.prediction,
            "explanation": prediction_response.explanation,
            "model": prediction_response.model,
            "assistant": rag_response,
        }