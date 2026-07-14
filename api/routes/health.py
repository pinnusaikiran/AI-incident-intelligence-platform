"""
Health check endpoints.
"""

from fastapi import APIRouter

from api.schemas import HealthResponse

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get(
    "",
    response_model=HealthResponse,
    summary="Health Check",
)
def health() -> HealthResponse:
    """
    Verify that the API is running.

    Returns
    -------
    HealthResponse
        API health status.
    """
    return HealthResponse(
        status="healthy"
    )