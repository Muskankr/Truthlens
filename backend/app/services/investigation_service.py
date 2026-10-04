from sqlalchemy.orm import Session

from app.models.investigation import Investigation
from app.models.evidence import Evidence

from app.services.retrieval_service import search_chunks
from app.services.conflict_service import find_conflicts
from app.services.confidence_service import calculate_confidence
from app.services.answer_service import generate_grounded_answer


def create_investigation(
    db: Session,
    question: str,
    limit: int = 5,
) -> dict:

    # ---------------------------------------------------------
    # 1. Retrieve relevant evidence
    # ---------------------------------------------------------

    retrieved_chunks = search_chunks(
        db=db,
        query=question,
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

    # ---------------------------------------------------------
    # 2. Average relevance
    # ---------------------------------------------------------

    if evidence:
        average_relevance = sum(
            item["relevance_score"]
            for item in evidence
        ) / len(evidence)
    else:
        average_relevance = 0.0

    # ---------------------------------------------------------
    # 3. Query-aware + temporal conflict detection
    # ---------------------------------------------------------

    relevant_chunk_ids = {
        item["chunk_id"]
        for item in evidence
    }

    all_conflicts = find_conflicts(
        db=db,
        relevant_chunk_ids=relevant_chunk_ids,
    )

    # Separate genuine unresolved conflicts from
    # historical/version supersession.
    potential_conflicts = [
        conflict
        for conflict in all_conflicts
        if conflict["status"] == "potential_conflict"
    ]

    superseded_claims = [
        conflict
        for conflict in all_conflicts
        if conflict["status"] == "superseded"
    ]

    # ---------------------------------------------------------
    # 4. Confidence
    # ---------------------------------------------------------

    confidence = calculate_confidence(
        evidence_count=len(evidence),
        average_relevance=average_relevance,
        conflict_count=len(potential_conflicts),
    )

    # ---------------------------------------------------------
    # 5. Grounded answer
    # ---------------------------------------------------------

    answer_result = generate_grounded_answer(
        question=question,
        evidence=evidence,
    )

    # ---------------------------------------------------------
    # 6. Investigation status
    # ---------------------------------------------------------

    if not evidence:
        status = "insufficient_evidence"

    elif potential_conflicts:
        status = "conflicting_evidence"

    else:
        status = "evidence_found"

    # ---------------------------------------------------------
    # 7. Missing evidence / verification notes
    # ---------------------------------------------------------

    missing_evidence = []

    if not evidence:
        missing_evidence.append(
            "No relevant document evidence was found."
        )

    elif len(evidence) == 1:
        missing_evidence.append(
            "Only one relevant evidence item was found."
        )

    if potential_conflicts:
        missing_evidence.append(
            "Conflicting claims require additional verification."
        )

    if superseded_claims:
        missing_evidence.append(
            f"{len(superseded_claims)} older claim(s) "
            "were identified as superseded by newer "
            "version or effective-date information."
        )

    # ---------------------------------------------------------
    # 8. Explain why this answer was produced
    # ---------------------------------------------------------

    why_this_answer = []

    if evidence:
        why_this_answer.append(
            f"{len(evidence)} relevant evidence item(s) "
            "were retrieved from the uploaded documents."
        )
    else:
        why_this_answer.append(
            "No relevant evidence was retrieved."
        )

    if average_relevance >= 0.75:
        why_this_answer.append(
            "The retrieved evidence has strong relevance "
            "to the question."
        )

    elif average_relevance >= 0.50:
        why_this_answer.append(
            "The retrieved evidence has moderate relevance "
            "to the question."
        )

    elif evidence:
        why_this_answer.append(
            "The retrieved evidence has weak relevance "
            "to the question."
        )

    # Genuine conflicts
    if potential_conflicts:
        why_this_answer.append(
            f"{len(potential_conflicts)} unresolved "
            "potential conflict(s) were detected among "
            "relevant claims."
        )
    else:
        why_this_answer.append(
            "No unresolved conflicting claims were detected "
            "in the relevant evidence."
        )

    # Superseded claims
    if superseded_claims:
        why_this_answer.append(
            f"{len(superseded_claims)} claim(s) were identified "
            "as superseded by newer version or "
            "effective-date information."
        )

    if answer_result["answer_type"] == "grounded_extract":
        why_this_answer.append(
            "The answer was constructed from the retrieved "
            "evidence rather than unsupported information."
        )

    elif answer_result["answer_type"] == "insufficient_evidence":
        why_this_answer.append(
            "The system could not construct a grounded answer "
            "because sufficient evidence was unavailable."
        )

    else:
        why_this_answer.append(
            f"Answer type: {answer_result['answer_type']}."
        )

    # ---------------------------------------------------------
    # 9. Create investigation record
    # ---------------------------------------------------------

    investigation = Investigation(
        question=question,
        answer=answer_result["answer"],
        confidence=confidence["score"],
        status=status,
    )

    db.add(investigation)
    db.flush()

    # ---------------------------------------------------------
    # 10. Store evidence records
    # ---------------------------------------------------------

    for item in evidence:

        db_evidence = Evidence(
            investigation_id=investigation.id,
            document_id=item["document_id"],
            chunk_id=item["chunk_id"],
            relevance_score=item["relevance_score"],
            support_type=item["support_type"],
        )

        db.add(db_evidence)

    db.commit()
    db.refresh(investigation)

    # ---------------------------------------------------------
    # 11. Return complete investigation
    # ---------------------------------------------------------

    return {
        "investigation_id": investigation.id,
        "question": question,
        "status": status,
        "answer": answer_result["answer"],
        "answer_type": answer_result["answer_type"],
        "supporting_evidence_ids": (
            answer_result["supporting_evidence_ids"]
        ),
        "confidence": confidence,
        "evidence": evidence,
        "conflicts": all_conflicts,
        "potential_conflicts": potential_conflicts,
        "superseded_claims": superseded_claims,
        "missing_evidence": missing_evidence,
        "why_this_answer": why_this_answer,
    }