from enum import Enum

class Priority(str, Enum):
    """
    Incident priority values.
    """
    CRITICAL = "1 - Critical"
    HIGH = "2 - High"
    MODERATE = "3 - Moderate"
    LOW = "4 - Low"

class Impact(str, Enum):
    """
    Incident impact values.
    """
    HIGH = "1 - High"
    MEDIUM = "2 - Medium"
    LOW = "3 - Low"

class Urgency(str, Enum):
    """
    Incident urgency values.
    """
    HIGH = "1 - High"
    MEDIUM = "2 - Medium"
    LOW = "3 - Low"

class ContactType(str, Enum):
    """
    Incident contact_type values.
    """
    DIRECT_OPENING = "Direct opening"
    PHONE = "Phone"
    EMAIL = "Email"
    IVR = "IVR"
    SELF_SERVICE = "Self service"