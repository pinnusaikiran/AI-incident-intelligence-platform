"""
Load all serialized machine learning artifacts required for inference.

This module is responsible for loading the trained CatBoost model,
preprocessing pipeline, feature schema, and metadata from disk.
"""

import json
from pathlib import Path
from functools import lru_cache
import joblib
import shap
from src.features.business_missing_value_transformer import BusinessMissingValueTransformer
from src.features.cyclic_encoder import CyclicEncoder
from src.inference.artifacts import InferenceArtifacts

PROJECT_ROOT=Path(__file__).resolve().parent.parent.parent
ARTIFACTS_DIR=PROJECT_ROOT/"artifacts"
MODELS_DIR=ARTIFACTS_DIR/"models"
MODEL_PATH=MODELS_DIR/"final_catboost_native.joblib"
PIPELINE_PATH=MODELS_DIR/"catboost_native_pipeline.joblib"
METADATA_PATH=MODELS_DIR/"metadata.json"

@lru_cache(maxsize=1)
def load_artifacts() -> InferenceArtifacts:
    """
    Load all serialized artifacts required for inference.

    Returns
    -------
    InferenceArtifacts
        Object containing the trained model,
        preprocessing pipeline,
        feature columns,
        and metadata required for inference.
    """
    try:
        with open(METADATA_PATH,'r') as file:
            metadata=json.load(file)
    
        model=joblib.load(MODEL_PATH)
        pipeline=joblib.load(PIPELINE_PATH)
        explainer = shap.TreeExplainer(model)

        artifacts=InferenceArtifacts(
            model=model,
            pipeline=pipeline,
            explainer=explainer,
            metadata=metadata
        )
        
        return artifacts
    except FileNotFoundError as e:
        raise FileNotFoundError(f" Required Artifact not found {e.filename}") from e
        
    


