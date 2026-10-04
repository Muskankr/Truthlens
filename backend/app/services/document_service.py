from pathlib import Path

from pypdf import PdfReader
from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.chunk import DocumentChunk


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def extract_pdf_pages(file_path: Path) -> list[dict]:
    reader = PdfReader(str(file_path))

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        pages.append(
            {
                "page_number": page_number,
                "text": text.strip(),
            }
        )

    return pages


def create_chunks(
    pages: list[dict],
    chunk_size: int = 1200,
    overlap: int = 200,
) -> list[dict]:

    chunks = []
    chunk_index = 0

    for page in pages:
        text = page["text"]

        if not text:
            continue

        start = 0

        while start < len(text):
            end = start + chunk_size

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append(
                    {
                        "content": chunk_text,
                        "page_number": page["page_number"],
                        "chunk_index": chunk_index,
                    }
                )

                chunk_index += 1

            if end >= len(text):
                break

            start = end - overlap

    return chunks


def process_document(
    db: Session,
    filename: str,
    file_path: Path,
) -> Document:

    try:
        pages = extract_pdf_pages(file_path)

        chunks = create_chunks(pages)

        document = Document(
            filename=filename,
            file_path=str(file_path),
            file_type="pdf",
            status="processing",
            page_count=len(pages),
        )

        db.add(document)
        db.flush()

        for chunk in chunks:
            db_chunk = DocumentChunk(
                document_id=document.id,
                content=chunk["content"],
                page_number=chunk["page_number"],
                chunk_index=chunk["chunk_index"],
            )

            db.add(db_chunk)

        # Never call an empty document "processed"
        if not chunks:
            document.status = "needs_ocr"
        else:
            document.status = "processed"

        db.commit()
        db.refresh(document)

        return document

    except Exception:
        db.rollback()
        raise