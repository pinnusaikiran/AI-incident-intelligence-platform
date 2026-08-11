"""
Mocked HTTP integration tests.

These tests verify the FastAPI API layer while replacing
external/expensive application services with mocks.
"""

from types import SimpleNamespace
from unittest.mock import Mock

from fastapi.testclient import TestClient

from api.main import app
from api.dependencies import get_prediction_service
from api.routes.intelligence import get_intelligence_service


client = TestClient(app,
    raise_server_exceptions=False)


VALID_PREDICTION_REQUEST = {
    "contact_type": "Phone",
    "location": "Location 204",
    "category": "Software",
    "subcategory": "Operating System",
    "u_symptom": "Symptom 208",
    "assignment_group": "Group 24",
    "assigned_to": "User 123",
    "caller_id": "Caller 456",
    "opened_by": "Opened By 789",
    "impact": "2 - Medium",
    "urgency": "2 - Medium",
    "priority": "2 - High",
    "Hour": 14,
    "Day_of_week": "Monday",
    "Month": "July",
}


def create_mock_prediction_response():
    """
    Create a deterministic prediction response.
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


def test_intelligence_endpoint_with_mocked_dependencies():
    """
    Verify the HTTP /intelligence/analyze endpoint while
    mocking PredictionService and RAGService.

    Real components:

        HTTP
        FastAPI
        Routing
        Dependency Injection
        Pydantic validation
        Response serialization

    Mocked components:

        PredictionService
        RAGService
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

    mock_rag_service.ask.return_value = SimpleNamespace(
        answer=(
            "Mocked intelligence response."
        ),
        sources=[],
    )

    # --------------------------------------------------
    # Override FastAPI dependencies
    # --------------------------------------------------

    def override_prediction_service():
        return mock_prediction_service

    def override_intelligence_service():
        from src.services.incident_intelligence_service import (
            IncidentIntelligenceService,
        )

        return IncidentIntelligenceService(
            prediction_service=mock_prediction_service,
            rag_service=mock_rag_service,
        )

    app.dependency_overrides[
        get_prediction_service
    ] = override_prediction_service

    app.dependency_overrides[
        get_intelligence_service
    ] = override_intelligence_service

    try:

        # --------------------------------------------------
        # Call real HTTP endpoint
        # --------------------------------------------------

        response = client.post(
            "/intelligence/analyze",
            params={
                "question": (
                    "What should I check "
                    "for this incident?"
                )
            },
            json=VALID_PREDICTION_REQUEST,
        )

        # --------------------------------------------------
        # HTTP response
        # --------------------------------------------------

        assert response.status_code == 200

        data = response.json()

        # --------------------------------------------------
        # Verify response contract
        # --------------------------------------------------

        assert "prediction" in data
        assert "explanation" in data
        assert "model" in data
        assert "assistant" in data

        # --------------------------------------------------
        # Verify prediction
        # --------------------------------------------------

        assert (
            data["prediction"]["prediction_class"]
            == 0
        )

        assert (
            data["prediction"]["prediction_label"]
            == "No SLA Breach"
        )

        assert (
            data["prediction"]["probability"]
            == 0.499481142153093
        )

        # --------------------------------------------------
        # Verify assistant
        # --------------------------------------------------

        assert (
            data["assistant"]["answer"]
            == "Mocked intelligence response."
        )

        assert (
            data["assistant"]["sources"]
            == []
        )

        # --------------------------------------------------
        # Verify dependencies were actually called
        # --------------------------------------------------

        mock_prediction_service.predict.assert_called_once()

        mock_rag_service.ask.assert_called_once()

        # --------------------------------------------------
        # Verify RAG received ML context
        # --------------------------------------------------

        rag_call = mock_rag_service.ask.call_args

        assert (
            rag_call.kwargs["question"]
            == "What should I check for this incident?"
        )

        incident_context = rag_call.kwargs[
            "incident_context"
        ]

        assert (
            incident_context["prediction_label"]
            == "No SLA Breach"
        )

        assert (
            incident_context["risk_level"]
            == "Borderline"
        )

        assert (
            incident_context[
                "sla_breach_probability"
            ]
            == 0.499481142153093
        )

    finally:

        # --------------------------------------------------
        # IMPORTANT:
        # Remove dependency overrides after the test.
        # --------------------------------------------------

        app.dependency_overrides.clear()


def test_intelligence_endpoint_rag_failure():
    """
    Verify that the intelligence endpoint handles a
    downstream RAG failure through the global exception
    handler.
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

    mock_rag_service.ask.side_effect = RuntimeError(
        "RAG service unavailable"
    )

    # --------------------------------------------------
    # Override FastAPI dependency
    # --------------------------------------------------

    def override_intelligence_service():

        from src.services.incident_intelligence_service import (
            IncidentIntelligenceService,
        )

        return IncidentIntelligenceService(
            prediction_service=mock_prediction_service,
            rag_service=mock_rag_service,
        )

    app.dependency_overrides[
        get_intelligence_service
    ] = override_intelligence_service

    try:

        response = client.post(
            "/intelligence/analyze",
            params={
                "question": (
                    "What should I check "
                    "for this incident?"
                )
            },
            json=VALID_PREDICTION_REQUEST,
        )

        # --------------------------------------------------
        # Global exception handler should return 500
        # --------------------------------------------------

        assert response.status_code == 500

        data = response.json()

        assert data["success"] is False

        assert (
            data["error"]["type"]
            == "InternalServerError"
        )

        assert (
            data["error"]["message"]
            == "An unexpected error occurred."
        )

        # --------------------------------------------------
        # Verify RAG was actually called
        # --------------------------------------------------

        mock_rag_service.ask.assert_called_once()

    finally:

        app.dependency_overrides.clear()