from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.conflict_service import find_conflicts


router = APIRouter()


@router.get("/conflicts")
def get_conflicts(
    db: Session = Depends(get_db),
):
    conflicts = find_conflicts(db)

    return {
        "count": len(conflicts),
        "conflicts": conflicts,
    }