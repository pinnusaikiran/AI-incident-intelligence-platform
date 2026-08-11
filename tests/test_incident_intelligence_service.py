"""
Mocked integration tests for IncidentIntelligenceService.
"""

from types import SimpleNamespace
from unittest.mock import Mock

from src.services.incident_intelligence_service import (
    IncidentIntelligenceService,
)


def create_mock_prediction_response():
    """
    Create a deterministic fake PredictionResponse.
    """

    prediction = SimpleNamespace(
        prediction_class=0,
        prediction_label="No SLA Breach",
        probability=0.499481142153093,
    )

    explanation = SimpleNamespace(
        base_value=-1.2451862860444056,
        feature_contributions=[
            SimpleNamespace(
                feature="assigned_to",
                impact=0.7565,
            ),
            SimpleNamespace(
                feature="priority",
                impact=0.7527,
            ),
            SimpleNamespace(
                feature="category",
                impact=-0.5314,
            ),
            SimpleNamespace(
                feature="assignment_group",
                impact=-0.4245,
            ),
            SimpleNamespace(
                feature="caller_id",
                impact=0.2900,
            ),
        ],
    )

    model = SimpleNamespace(
        name="CatBoost Native",
        version="1.0.0",
    )

    return SimpleNamespace(
        prediction=prediction,
        explanation=explanation,
        model=model,
    )


def test_incident_intelligence_service_orchestration():
    """
    Verify:

        PredictionService
              ↓
        risk context
              ↓
        RAGService
              ↓
        combined response
    """

    # --------------------------------------------------
    # Mock PredictionService
    # --------------------------------------------------

    mock_prediction_service = Mock()

    mock_prediction_service.predict.return_value = (
        create_mock_prediction_response()
    )

    # --------------------------------------------------
    # Mock RAGService
    # --------------------------------------------------

    mock_rag_service = Mock()

    mock_rag_response = SimpleNamespace(
        answer="Mocked incident intelligence response.",
        sources=[],
    )

    mock_rag_service.ask.return_value = mock_rag_response

    # --------------------------------------------------
    # Create service
    # --------------------------------------------------

    service = IncidentIntelligenceService(
        prediction_service=mock_prediction_service,
        rag_service=mock_rag_service,
    )

    # --------------------------------------------------
    # Execute
    # --------------------------------------------------

    request = Mock()

    result = service.analyze(
        request=request,
        question="What should I check?",
    )

    # --------------------------------------------------
    # Verify PredictionService was called
    # --------------------------------------------------

    mock_prediction_service.predict.assert_called_once_with(
        request
    )

    # --------------------------------------------------
    # Verify RAGService was called
    # --------------------------------------------------

    mock_rag_service.ask.assert_called_once()

    rag_call = mock_rag_service.ask.call_args

    assert rag_call.kwargs["question"] == (
        "What should I check?"
    )

    incident_context = rag_call.kwargs[
        "incident_context"
    ]

    # --------------------------------------------------
    # Verify deterministic risk calculation
    # --------------------------------------------------

    assert (
        incident_context["prediction_class"]
        == 0
    )

    assert (
        incident_context["prediction_label"]
        == "No SLA Breach"
    )

    assert (
        incident_context["sla_breach_probability"]
        == 0.499481142153093
    )

    assert (
        incident_context["decision_threshold"]
        == 0.5
    )

    assert (
        incident_context["risk_level"]
        == "Borderline"
    )

    # --------------------------------------------------
    # Verify SHAP contributors
    # --------------------------------------------------

    contributors = incident_context[
        "top_shap_contributors"
    ]

    assert len(contributors) == 5

    assert contributors[0]["feature"] == "assigned_to"
    assert contributors[1]["feature"] == "priority"

    # --------------------------------------------------
    # Verify final response
    # --------------------------------------------------

    assert result["prediction"] == (
        mock_prediction_service.predict.return_value.prediction
    )

    assert result["explanation"] == (
        mock_prediction_service.predict.return_value.explanation
    )

    assert result["model"] == (
        mock_prediction_service.predict.return_value.model
    )

    assert result["assistant"] == mock_rag_response