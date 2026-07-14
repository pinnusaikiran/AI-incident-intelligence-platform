"""
Dataclass definitions for model explanations.

This module contains data structures used to represent SHAP feature contributions returned during inference.
"""

from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class FeatureContribution:
    """
    Stores the SHAP contribution of a single feature.

    Attributes
    ----------
    feature : str
        Name of the feature.

    impact : float
        SHAP value representing the feature's
        contribution towards the prediction.
    """
    feature:str
    impact:float

@dataclass(frozen=True)
class ExplanationResult:
    """
    Stores the SHAP explanation generated for
    a single prediction.

    Attributes
    ----------
    base_value : float
        Base prediction before feature contributions.

    feature_contributions : list[FeatureContribution]
        SHAP contribution of every feature.
    """
    base_value: float
    feature_contributions: list[FeatureContribution]