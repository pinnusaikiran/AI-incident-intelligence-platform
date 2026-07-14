import pandas as pd
import shap
from src.inference.explanation import ExplanationResult,FeatureContribution
from src.inference.artifacts import InferenceArtifacts

def generate_explanation(transformed_df:pd.DataFrame,artifacts:InferenceArtifacts) -> ExplanationResult:
    """
    Generate SHAP explanations for a single prediction.

    Parameters
    ----------
    transformed_df : pd.DataFrame
        Preprocessed feature matrix used for prediction.

    artifacts : InferenceArtifacts
        Loaded inference artifacts.

    Returns
    -------
    ExplanationResult
        Base prediction value together with SHAP feature
        contributions sorted by absolute impact.
    """
    shap_values = artifacts.explainer(transformed_df)
    base_value = float(shap_values.base_values[0])
    values = shap_values.values[0]
    feature_names = transformed_df.columns

    contributions = [FeatureContribution(feature=feature,impact=float(value)) 
                     for feature, value in zip(feature_names, values)]

    contributions.sort(key=lambda item: abs(item.impact),reverse=True)

    return ExplanationResult(base_value=base_value,feature_contributions=contributions)