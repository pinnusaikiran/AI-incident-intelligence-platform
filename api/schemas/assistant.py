"""
Assistant API schemas.
"""

from pydantic import BaseModel, Field


class AssistantRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=3,
        description="Question about an IT incident.",
    )

    incident_context: dict | None = None


class AssistantSource(BaseModel):

    source: str

    score: float

    text: str


class AssistantResponse(BaseModel):

    answer: str

    sources: list[AssistantSource]