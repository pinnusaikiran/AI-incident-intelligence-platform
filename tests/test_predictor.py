import pytest

from src.inference.prediction import PredictionResult
from tests.conftest import artifacts,valid_data,invalid_data
from src.inference.predictor import predict


def test_predict(artifacts, valid_data, invalid_data):

    result = predict(
        request_data=valid_data,
        artifacts=artifacts
    )

    assert isinstance(result, PredictionResult)
    assert isinstance(result.prediction, int)
    assert isinstance(result.probability, float)
    assert 0.0 <= result.probability <= 1.0
    assert result.prediction in (0, 1)

    with pytest.raises(ValueError, match="Invalid datatype"):
        predict(
            request_data=invalid_data,
            artifacts=artifacts
        )