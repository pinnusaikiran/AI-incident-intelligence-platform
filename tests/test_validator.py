import pandas as pd
import pytest

from src.inference.validator import (
    build_dataframe,
    reorder_features,
    validate_data_types,
    validate_request,
    validate_required_fields,
    validate_unknown_fields,
)

def test_validate_request(
    valid_data,
    metadata,
    feature_columns,
):
    df = validate_request(
        valid_data,
        metadata,
    )

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert list(df.columns) == feature_columns

def test_validate_required_fields(
    valid_data,
    feature_columns,
    missing_field_data,
):
    
    validate_required_fields(
    valid_data,
    feature_columns,
)
    with pytest.raises(ValueError):
        validate_required_fields(missing_field_data,feature_columns)

def test_validate_unknown_fields(
    valid_data,
    feature_columns,
    unknown_field_data,
):
    validate_unknown_fields(valid_data,feature_columns)
    with pytest.raises(ValueError,match="Unknown fields received"):
        validate_unknown_fields(unknown_field_data,feature_columns)

def test_reorder_features(
    valid_data,
    feature_columns,
):
    ordered=reorder_features(valid_data,feature_columns)
    assert list(ordered.keys())==feature_columns,"Not able to reorder the features"

def test_build_dataframe(
    valid_data,
    feature_columns,
):
    ordered_data = reorder_features(valid_data, feature_columns)
    df=build_dataframe(ordered_data)
    assert isinstance(df,pd.DataFrame),"It is not an Dataframe"
    assert len(df)==1,"Dataframe does not contain only one record"
    assert list(df.columns)== list(feature_columns)

def test_validate_data_types(
    valid_data,
    metadata,
    invalid_type_data,
):
    validate_data_types(valid_data,metadata)
    with pytest.raises(ValueError, match="Invalid datatype"):
        validate_data_types(invalid_type_data, metadata)