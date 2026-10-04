from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.evidence_service import build_evidence_set


router = APIRouter()


@router.get("/evidence")
def get_evidence(
    q: str = Query(..., min_length=1),
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
):
    evidence = build_evidence_set(
        db=db,
        query=q,
        limit=limit,
    )

    return {
        "query": q,
        "evidence_count": len(evidence),
        "evidence": evidence,
    }