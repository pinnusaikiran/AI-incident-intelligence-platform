from pydantic import BaseModel
from api.schemas.enums import Priority,Urgency,Impact,ContactType

class PredictionRequest(BaseModel):
    """
    Prediction request payload.
    """

    contact_type: ContactType
    location: str
    category: str
    subcategory: str
    u_symptom: str
    assignment_group: str
    assigned_to: str
    caller_id: str
    opened_by: str
    impact: Impact
    urgency: Urgency
    priority: Priority
    Hour: int
    Day_of_week: str
    Month: str