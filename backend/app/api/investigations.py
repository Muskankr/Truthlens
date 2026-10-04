from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import select


from app.db.session import get_db
from app.services.investigation_service import create_investigation
from app.models.investigation import Investigation


router = APIRouter()


class InvestigationRequest(BaseModel):
    question: str = Field(..., min_length=3)
    limit: int = Field(default=5, ge=1, le=20)


@router.post("/investigations")
def investigate(
    request: InvestigationRequest,
    db: Session = Depends(get_db),
):
    return create_investigation(
        db=db,
        question=request.question,
        limit=request.limit,
    )

@router.get("")
def list_investigations(
    db: Session = Depends(get_db),
):
    investigations = db.execute(
        select(Investigation).order_by(
            Investigation.created_at.desc()
        )
    ).scalars().all()

    return {
        "count": len(investigations),
        "investigations": [
            {
                "id": investigation.id,
                "question": investigation.question,
                "answer": investigation.answer,
                "confidence": investigation.confidence,
                "status": investigation.status,
                "created_at": (
                    investigation.created_at.isoformat()
                    if investigation.created_at
                    else None
                ),
            }
            for investigation in investigations
        ],
    }