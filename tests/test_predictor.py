import pytest

from src.inference.prediction import PredictionResult
from src.inference.predictor import predict
from src.inference.validator import validate_request


def test_predict(artifacts, valid_data, invalid_type_data):

    df = validate_request(request_data=valid_data, metadata=artifacts.metadata)
    transformed_df = artifacts.pipeline.transform(df)

    result = predict(
        transformed_df=transformed_df,
        artifacts=artifacts
    )

    assert isinstance(result, PredictionResult)
    assert isinstance(result.prediction, int)
    assert isinstance(result.probability, float)
    assert 0.0 <= result.probability <= 1.0
    assert result.prediction in (0, 1)

    with pytest.raises(ValueError, match="Invalid datatype"):
        validate_request(
            request_data=invalid_type_data,
            metadata=artifacts.metadata,
        )