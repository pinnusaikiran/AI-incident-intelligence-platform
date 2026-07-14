"""
Dataclass definitions for the inference module.

This module contains data structures used to store
the machine learning artifacts required during inference.
"""

from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class InferenceArtifacts:
    """
    Stores all artifacts required during inference.

    Attributes
    ----------
    model : Any
        Trained CatBoost model.

    pipeline : Any
        Preprocessing pipeline.

    explainer : Any
        SHAP TreeExplainer used to generate
        feature contribution explanations.

    metadata : dict[str, Any]
        Model metadata and input schema.
    """
    model: Any
    pipeline: Any
    explainer: Any
    metadata: dict[str, Any]
    
    
