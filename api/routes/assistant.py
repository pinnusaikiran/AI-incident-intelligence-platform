"""
AI Incident Intelligence Assistant endpoints.
"""

from fastapi import APIRouter, Depends

from api.schemas.assistant import (
    AssistantRequest,
    AssistantResponse,
)

from rag.rag_service import RAGService


router = APIRouter(
    prefix="/assistant",
    tags=["AI Assistant"],
)


rag_service = RAGService()


@router.post(
    "/ask",
    response_model=AssistantResponse,
    summary="Ask the AI Incident Intelligence Assistant",
)
def ask_assistant(
    request: AssistantRequest,
):

    prediction_context = None

    if request.incident_context:

        prediction_context = (
            "Incident information:\n"
            f"{request.incident_context}"
        )

    response = rag_service.ask(
        question=request.question,
        incident_context=prediction_context,
    )

    return AssistantResponse(
        answer=response.answer,
        sources=[
            {
                "source": source.source,
                "score": source.score,
                "text": source.text,
            }
            for source in response.sources
        ],
    )