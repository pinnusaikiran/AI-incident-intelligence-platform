"""
FastAPI dependency providers.

This module contains reusable dependencies shared
across API routes.
"""

from src.inference.artifacts import InferenceArtifacts
from src.inference.loader import load_artifacts


def get_artifacts() -> InferenceArtifacts:
    """
    Return cached inference artifacts.

    Returns
    -------
    InferenceArtifacts
        Loaded model, preprocessing pipeline,
        SHAP explainer, and metadata.
    """
    return load_artifacts()