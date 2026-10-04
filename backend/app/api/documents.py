from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.document import Document
from app.services.document_service import UPLOAD_DIR, process_document


router = APIRouter()


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required.",
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    safe_filename = (
        f"{uuid4()}_{Path(file.filename).name}"
    )

    file_path = UPLOAD_DIR / safe_filename

    try:
        with file_path.open("wb") as buffer:
            while chunk := await file.read(
                1024 * 1024
            ):
                buffer.write(chunk)

        document = process_document(
            db=db,
            filename=file.filename,
            file_path=file_path,
        )

        return {
            "id": document.id,
            "filename": document.filename,
            "file_type": document.file_type,
            "status": document.status,
            "page_count": document.page_count,
        }

    except Exception as exc:
        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=500,
            detail=f"Document processing failed: {exc}",
        ) from exc


@router.get("")
def list_documents(
    db: Session = Depends(get_db),
):
    documents = db.execute(
        select(Document).order_by(
            Document.created_at.desc()
        )
    ).scalars().all()

    return {
        "count": len(documents),
        "documents": [
            {
                "id": document.id,
                "filename": document.filename,
                "file_type": document.file_type,
                "status": document.status,
                "page_count": document.page_count,
                "created_at": (
                    document.created_at.isoformat()
                    if document.created_at
                    else None
                ),
            }
            for document in documents
        ],
    }