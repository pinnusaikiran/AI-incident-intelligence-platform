import pytest
from src.inference.prediction import PredictionResult
from src.inference.explanation import ExplanationResult,FeatureContribution
from src.inference.response_builder import build_response
from src.inference.response import APIResponse,ModelInfo,PredictionInfo

@pytest.fixture(scope='session')
def prediction():
    return PredictionResult(prediction=1,probability=0.912)

@pytest.fixture(scope='session')
def explanation():
    return ExplanationResult(base_value=2.13,feature_contributions=[
        FeatureContribution(feature="priority",
                            impact=1.42),
        FeatureContribution(feature="impact",
                            impact=0.86)
                            ])

@pytest.fixture(scope="session")
def metadata():
    return {
        "model_name": "CatBoost Native",
        "model_version": "1.0.0",
        "positive_class": "SLA Breach",
    }


def test_build_response(prediction,explanation,metadata):

    response = build_response(
        prediction=prediction,
        explanation=explanation,
        metadata=metadata,
    )

    assert isinstance(response, APIResponse)

    assert isinstance(
        response.prediction,
        PredictionInfo,
    )

    assert isinstance(
        response.explanation,
        ExplanationResult,
    )

    assert isinstance(
        response.model,
        ModelInfo,
    )

    assert response.prediction.prediction_class == 1

    assert response.prediction.prediction_label == "SLA Breach"

    assert response.prediction.probability == prediction.probability

    assert response.model.name == "CatBoost Native"

    assert response.model.version == "1.0.0"

    assert len(response.explanation.feature_contributions) == 2

    assert (response.explanation is explanation)

def test_build_response_negative_prediction(
    explanation,
    metadata,
):

    prediction = PredictionResult(
        prediction=0,
        probability=0.083
    )

    response = build_response(
        prediction=prediction,
        explanation=explanation,
        metadata=metadata,
    )

    assert response.prediction.prediction_class == 0

    assert response.prediction.prediction_label == "No SLA Breach"