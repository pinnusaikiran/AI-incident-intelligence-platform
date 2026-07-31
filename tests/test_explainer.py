import pytest
import pandas as pd
import math
from tests.conftest import artifacts
from src.inference.validator import validate_request
from src.inference.explainer import generate_explanation
from src.inference.explanation import (FeatureContribution,ExplanationResult)


def test_generate_explaintion(artifacts,valid_data):
    df=validate_request(request_data=valid_data,metadata=artifacts.metadata)
    transformed_df=artifacts.pipeline.transform(df)

    explanation=generate_explanation(transformed_df=transformed_df,artifacts=artifacts)

    assert isinstance(explanation,ExplanationResult)
    assert isinstance(explanation.base_value,float)
    assert len(explanation.feature_contributions)>0
    assert all(isinstance(feature,FeatureContribution) for feature in explanation.feature_contributions)

    impacts= [abs(feature.impact) for feature in explanation.feature_contributions]

    assert impacts==sorted(impacts,reverse=True)
    feature_names = {feature.feature for feature in explanation.feature_contributions}

    assert feature_names == set(transformed_df.columns)
    assert len(explanation.feature_contributions) == len(transformed_df.columns)
    assert all(
    isinstance(feature.impact, float)
    for feature in explanation.feature_contributions
)
    assert math.isfinite(explanation.base_value)

def test_generate_explanation_invalid_request(
    artifacts,
    invalid_type_data,
):
    with pytest.raises(ValueError):
        df = validate_request(
            request_data=invalid_type_data,
            metadata=artifacts.metadata,
        )