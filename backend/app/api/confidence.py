from fastapi import APIRouter, Query

from app.services.confidence_service import calculate_confidence


router = APIRouter()


@router.get("/confidence")
def get_confidence(
    evidence_count: int = Query(0, ge=0),
    average_relevance: float = Query(0.0, ge=0.0, le=1.0),
    conflict_count: int = Query(0, ge=0),
):
    result = calculate_confidence(
        evidence_count=evidence_count,
        average_relevance=average_relevance,
        conflict_count=conflict_count,
    )

    return result