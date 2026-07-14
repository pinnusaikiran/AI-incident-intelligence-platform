from pydantic import BaseModel


class PredictionRequest(BaseModel):
    """
    Prediction request payload.
    """

    contact_type: str
    location: str
    category: str
    subcategory: str
    u_symptom: str
    assignment_group: str
    assigned_to: str
    caller_id: str
    opened_by: str
    impact: int
    urgency: int
    priority: int
    Hour: int
    Day_of_week: str
    Month: str