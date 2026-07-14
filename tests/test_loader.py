from src.inference.loader import load_artifacts
from tests.conftest import artifacts
import pytest




def test_model_loaded(artifacts):
    assert artifacts.model is not None,"Model failed to load."
    assert hasattr(artifacts.model,"predict"),"Model does not implement predict()."
    assert hasattr(artifacts.model,"predict_proba"),"Model does not implement predict_proba()."

def test_pipeline_loaded(artifacts):
    assert artifacts.pipeline is not None,"Pipeline failed to load"
    assert hasattr(artifacts.pipeline,"transform"), "Pipeline doesn't implement transform()"
    

def test_metadata_loaded(artifacts):
    assert isinstance(artifacts.metadata,dict),"Metadata is not a dictionary"
    assert ("model_name" in artifacts.metadata), "Metadata missing 'model_name'."
    assert ("algorithm" in artifacts.metadata),"Metadata missing 'algorithm'."
    assert ("number_of_features" in artifacts.metadata),"Metadata missing 'number_of_features'."
    assert len(artifacts.metadata["input_schema"]) == artifacts.metadata["number_of_features"]
    
def test_explainer_loaded(artifacts):
    assert artifacts.explainer is not None
    assert hasattr(artifacts.explainer,"shap_values") or hasattr(artifacts.explainer,"__call__")