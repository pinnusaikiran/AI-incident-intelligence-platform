import pytest
from src.inference.loader import load_artifacts

@pytest.fixture(scope='session')
def artifacts():
    """Load inference artifacts once per test session."""
    return load_artifacts()

@pytest.fixture(scope='session')
def valid_data():
    """Valid inference payload used across tests."""
    return {
        "contact_type": "Phone",
        "location": "Location 204",
        "category": "Category 55",
        "subcategory": "Subcategory 170",
        "u_symptom": "Symptom 208",
        "assignment_group": "Group 70",
        "assigned_to": "User 1",
        "caller_id": "Caller 15",
        "opened_by": "User 20",
        "impact": 2,
        "urgency": 2,
        "priority": 2,
        "Hour": 13,
        "Day_of_week": "Sunday",
        "Month": "May",
    }

@pytest.fixture(scope="session")
def invalid_type_data(valid_data):
    """Payload containing an invalid datatype."""
    payload = valid_data.copy()
    payload["impact"] = "High"
    return payload

@pytest.fixture(scope="session")
def missing_field_data(valid_data):
    """Payload missing one required field."""
    payload = valid_data.copy()
    payload.pop("impact")
    return payload

@pytest.fixture(scope="session")
def unknown_field_data(valid_data):
    """Payload containing an unexpected field."""
    payload = valid_data.copy()
    payload["salary"] = 100000
    return payload

@pytest.fixture(scope="session")
def metadata(artifacts):
    """Model metadata loaded from serialized artifacts."""
    return artifacts.metadata

@pytest.fixture(scope="session")
def feature_columns(metadata):
    """Feature order derived from production metadata."""
    return list(metadata["input_schema"].keys())