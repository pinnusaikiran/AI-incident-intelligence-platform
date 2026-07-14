"""
Validating all the requirements for predicting the output.

This module is responsible for validating required fields,unknown_fields,data_types,
order of features,and converting the input data into dataframe.
"""

from typing import Any
import pandas as pd

TYPE_MAPPING: dict[str, type] = {
        "str": str,
        "float": float,
        "int": int,
        "bool": bool
    }

def validate_request(request_data: dict[str, Any],metadata: dict[str, Any]) -> pd.DataFrame:
    """
    Validate the incoming request and convert it into a
    single-row pandas DataFrame suitable for inference.

    Parameters
    ----------
    request_data : dict
        Incoming request payload.

    metadata : dict
        Model metadata containing the input schema.
        Feature order is derived from the schema.

    Returns
    -------
    pd.DataFrame
        Validated DataFrame in the correct feature order.

    Raises
    ------
    ValueError
        If validation fails.
    """
    feature_columns = list(metadata["input_schema"].keys())

    validate_required_fields(
        request_data,
        feature_columns,
    )

    validate_unknown_fields(
        request_data,
        feature_columns,
    )

    validate_data_types(
        request_data,
        metadata,
    )

    ordered_data = reorder_features(
        request_data,
        feature_columns,
    )
    return build_dataframe(ordered_data)

def validate_required_fields(request_data:dict[str,Any],feature_columns:list[str])-> None:
    """
    Validate that all required features are present
    in the incoming request.

    Raises
    ------
    ValueError
        If one or more required fields are missing.
    """
     
    missing_fields = set(feature_columns) - set(request_data)
    if missing_fields:  
        raise ValueError(f"Missing required fields: {sorted(missing_fields)}")
    
    
    
    
def validate_unknown_fields(request_data:dict[str,Any],feature_columns:list[str])-> None:
    """
    Validate whether unknown features are present
    in the incoming request.

    Raises
    ------
    ValueError
        If unknown fields are available.
    """
    unknown_fields = set(request_data) - set(feature_columns)
    if unknown_fields:
        raise ValueError(f"Unknown fields received: {sorted(unknown_fields)}")
    

def reorder_features(request_data:dict[str,Any],feature_columns:list[str])-> dict[str,Any]:
    """
    Reorder the validated request according to the training feature order.

    Returns
    -------
    dict[str, Any]
        Dictionary with features arranged in the
        expected order.
    """
    return {feature:request_data[feature] for feature  in feature_columns}



def build_dataframe(ordered_data: dict[str, Any]) -> pd.DataFrame:
    """
    This function builds ordered dictionary into dataframe .

    Returns
    -------
    pd.DataFrame
        Single-row DataFrame containing the validated
        request in the expected feature order.
    """
    return pd.DataFrame([ordered_data])

def validate_data_types(request_data:dict[str,Any],metadata:dict[str,Any])-> None:
    """
    Validate the datatype of each input feature.

    Raises
    ------
    ValueError
        If the datatype of any feature does not
        match the schema defined in metadata.
    """
    
    for field,schema in metadata['input_schema'].items():
        actual_value = request_data[field]
        expected_type = TYPE_MAPPING.get(schema["type"])

        if expected_type is None:
            raise ValueError(
                f"Unsupported datatype '{schema['type']}' "
                "found in metadata."
            )

        if not isinstance(actual_value,expected_type):
            raise ValueError(
                f"Invalid datatype for '{field}'. "
                f"Expected {expected_type.__name__}, "
                f"received {type(actual_value).__name__}."
)
    




