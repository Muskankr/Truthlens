from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.retrieval_service import search_chunks


router = APIRouter()


@router.get("/search")
def search_documents(
    q: str = Query(..., min_length=1),
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
):
    results = search_chunks(
        db=db,
        query=q,
        limit=limit,
    )

    return {
        "query": q,
        "count": len(results),
        "results": results,
    }