"""
Integration tests for the AI Incident Intelligence Platform API.

These tests verify that the major application components work together
through the FastAPI HTTP layer.
"""

from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


# ---------------------------------------------------------
# Valid PredictionRequest used by the existing /predict API
# ---------------------------------------------------------

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


# =========================================================
# /predict
# =========================================================

def test_predict_endpoint_integration():
    """
    Verify the complete /predict HTTP flow.

    FastAPI
        -> validation
        -> prediction service
        -> CatBoost
        -> SHAP
        -> response builder
        -> JSON response
    """

    response = client.post(
        "/predict",
        json=VALID_PREDICTION_REQUEST,
    )

    assert response.status_code == 200

    data = response.json()

    # Top-level response contract
    assert "prediction" in data
    assert "explanation" in data
    assert "model" in data

    # Prediction contract
    prediction = data["prediction"]

    assert "prediction_class" in prediction
    assert "prediction_label" in prediction
    assert "probability" in prediction

    assert prediction["prediction_class"] in [0, 1]
    assert prediction["prediction_label"] in [
        "SLA Breach",
        "No SLA Breach",
    ]

    assert 0.0 <= prediction["probability"] <= 1.0

    # Explanation contract
    explanation = data["explanation"]

    assert "base_value" in explanation
    assert "feature_contributions" in explanation

    assert isinstance(
        explanation["feature_contributions"],
        list,
    )

    assert len(
        explanation["feature_contributions"]
    ) > 0

    # Model contract
    model = data["model"]

    assert "name" in model
    assert "version" in model


# =========================================================
# /assistant/ask
# =========================================================

def test_assistant_endpoint_integration():
    """
    Verify the AI Assistant HTTP flow.

    FastAPI
        -> AssistantRequest validation
        -> RAGService
        -> embedding retrieval
        -> LLM
        -> AssistantResponse
    """

    payload = {
        "question": (
            "What should I check when an incident "
            "has high SLA risk?"
        )
    }

    response = client.post(
        "/assistant/ask",
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert "sources" in data

    assert isinstance(data["answer"], str)
    assert len(data["answer"]) > 0

    assert isinstance(data["sources"], list)

    assert len(data["sources"]) > 0

    # Validate source structure
    source = data["sources"][0]

    assert "source" in source
    assert "score" in source
    assert "text" in source

    assert isinstance(source["source"], str)
    assert isinstance(source["score"], (int, float))
    assert isinstance(source["text"], str)


# =========================================================
# /intelligence/analyze
# =========================================================

def test_intelligence_analyze_endpoint_integration():
    """
    Verify the complete Incident Intelligence workflow.

    FastAPI
        -> PredictionRequest validation
        -> PredictionService
        -> CatBoost
        -> SHAP
        -> risk context
        -> RAG retrieval
        -> LLM
        -> combined response
    """

    response = client.post(
        "/intelligence/analyze",
        params={
            "question": (
                "What should I check when an incident "
                "has high SLA risk?"
            )
        },
        json=VALID_PREDICTION_REQUEST,
    )

    assert response.status_code == 200

    data = response.json()

    # -----------------------------------------------------
    # Top-level V2 response
    # -----------------------------------------------------

    assert "prediction" in data
    assert "explanation" in data
    assert "model" in data
    assert "assistant" in data

    # -----------------------------------------------------
    # Prediction
    # -----------------------------------------------------

    prediction = data["prediction"]

    assert "prediction_class" in prediction
    assert "prediction_label" in prediction
    assert "probability" in prediction

    assert prediction["prediction_class"] in [0, 1]
    assert 0.0 <= prediction["probability"] <= 1.0

    # -----------------------------------------------------
    # SHAP explanation
    # -----------------------------------------------------

    explanation = data["explanation"]

    assert "base_value" in explanation
    assert "feature_contributions" in explanation

    contributions = explanation[
        "feature_contributions"
    ]

    assert isinstance(contributions, list)
    assert len(contributions) > 0

    for contribution in contributions:

        assert "feature" in contribution
        assert "impact" in contribution

        assert isinstance(
            contribution["feature"],
            str,
        )

        assert isinstance(
            contribution["impact"],
            (int, float),
        )

    # -----------------------------------------------------
    # Model information
    # -----------------------------------------------------

    model = data["model"]

    assert "name" in model
    assert "version" in model

    # -----------------------------------------------------
    # Assistant / RAG response
    # -----------------------------------------------------

    assistant = data["assistant"]

    assert "answer" in assistant
    assert "sources" in assistant

    assert isinstance(
        assistant["answer"],
        str,
    )

    assert len(assistant["answer"]) > 0

    assert isinstance(
        assistant["sources"],
        list,
    )

    assert len(assistant["sources"]) > 0


# =========================================================
# Invalid request tests
# =========================================================

def test_predict_endpoint_invalid_request():
    """
    Verify that /predict rejects an invalid request.
    """

    response = client.post(
        "/predict",
        json={},
    )

    assert response.status_code == 422


def test_intelligence_endpoint_invalid_request():
    """
    Verify that /intelligence/analyze rejects an invalid
    PredictionRequest.
    """

    response = client.post(
        "/intelligence/analyze",
        params={
            "question": "What should I check?"
        },
        json={},
    )

    assert response.status_code == 422


# =========================================================
# Assistant validation
# =========================================================

def test_assistant_endpoint_invalid_request():
    """
    Verify that /assistant/ask rejects an invalid request.
    """

    response = client.post(
        "/assistant/ask",
        json={},
    )

    assert response.status_code == 422