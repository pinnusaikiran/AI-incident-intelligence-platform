"""
Load all serialized machine learning artifacts required for inference.

This module is responsible for loading the trained CatBoost model,
preprocessing pipeline, feature schema, and metadata from disk.
"""
import logging
import json
from pathlib import Path
from functools import lru_cache
import joblib
import shap
from src.features.business_missing_value_transformer import BusinessMissingValueTransformer
from src.features.cyclic_encoder import CyclicEncoder
from src.inference.artifacts import InferenceArtifacts


logger = logging.getLogger(__name__)


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
        logger.info("Loading metadata...")
        with open(METADATA_PATH,'r') as file:
            metadata=json.load(file)

        logger.info("Metadata loaded")  

        logger.info("Loading CatBoost model...")
        model=joblib.load(MODEL_PATH)

        logger.info("CatBoost model loaded from %s",MODEL_PATH.name,)

        logger.info("Loading preprocessing pipeline...")
        pipeline=joblib.load(PIPELINE_PATH)
        logger.info("Pipeline loaded from %s",PIPELINE_PATH.name,)

        logger.info("Initializing SHAP explainer...")
        explainer = shap.TreeExplainer(model)
        logger.info("SHAP explainer initialized")

        artifacts=InferenceArtifacts(
            model=model,
            pipeline=pipeline,
            explainer=explainer,
            metadata=metadata
        )
        
        return artifacts
    except FileNotFoundError as e:
        raise FileNotFoundError(f" Required Artifact not found {e.filename}") from e
        
    


