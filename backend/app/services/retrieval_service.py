from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.chunk import DocumentChunk


def search_chunks(
    db: Session,
    query: str,
    limit: int = 5,
) -> list[dict]:
    """
    Simple keyword-based retrieval.

    This is intentionally our first retrieval layer.
    Later TruthLens will upgrade this to hybrid retrieval
    using keyword + vector similarity + reranking.
    """

    query_words = [
        word.strip().lower()
        for word in query.split()
        if len(word.strip()) >= 3
    ]

    if not query_words:
        return []

    stmt = select(DocumentChunk).order_by(DocumentChunk.id)

    chunks = db.execute(stmt).scalars().all()

    results = []

    for chunk in chunks:
        content_lower = chunk.content.lower()

        matched_words = [
            word
            for word in query_words
            if word in content_lower
        ]

        if not matched_words:
            continue

        score = len(matched_words) / len(query_words)

        results.append(
            {
                "chunk_id": chunk.id,
                "document_id": chunk.document_id,
                "page_number": chunk.page_number,
                "content": chunk.content,
                "score": round(score, 4),
                "matched_words": matched_words,
            }
        )

    results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return results[:limit]