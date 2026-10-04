from sqlalchemy.orm import Session

from app.services.retrieval_service import search_chunks


def build_evidence_set(
    db: Session,
    query: str,
    limit: int = 5,
) -> list[dict]:
    """
    Retrieve relevant document chunks and convert them
    into structured evidence items.
    """

    retrieved_chunks = search_chunks(
        db=db,
        query=query,
        limit=limit,
    )

    evidence = []

    for item in retrieved_chunks:
        evidence.append(
            {
                "chunk_id": item["chunk_id"],
                "document_id": item["document_id"],
                "page_number": item["page_number"],
                "content": item["content"],
                "relevance_score": item["score"],
                "support_type": "potential_support",
            }
        )

    return evidence