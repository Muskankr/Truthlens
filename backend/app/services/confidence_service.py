def calculate_confidence(
    evidence_count: int,
    average_relevance: float,
    conflict_count: int,
) -> dict:
    """
    Calculate an explainable confidence score.

    This is V1 of the TruthLens confidence engine.
    The score is intentionally deterministic and explainable.
    """

    score = 0.0

    # Evidence coverage
    if evidence_count >= 5:
        score += 40
    elif evidence_count >= 3:
        score += 32
    elif evidence_count >= 2:
        score += 24
    elif evidence_count == 1:
        score += 15

    # Evidence relevance
    score += min(
        max(average_relevance, 0.0),
        1.0
    ) * 40

    # Conflict penalty
    if conflict_count == 0:
        score += 20
    elif conflict_count == 1:
        score += 8
    else:
        score -= 5 * min(conflict_count, 5)

    score = max(0.0, min(score, 100.0))

    if score >= 80:
        level = "high"
    elif score >= 60:
        level = "medium"
    else:
        level = "low"

    reasons = []

    if evidence_count == 0:
        reasons.append("No supporting evidence was found.")
    elif evidence_count == 1:
        reasons.append("Only one relevant evidence item was found.")
    else:
        reasons.append(
            f"{evidence_count} relevant evidence items were found."
        )

    if average_relevance >= 0.75:
        reasons.append("Evidence relevance is strong.")
    elif average_relevance >= 0.5:
        reasons.append("Evidence relevance is moderate.")
    else:
        reasons.append("Evidence relevance is weak.")

    if conflict_count == 0:
        reasons.append("No conflicting claims were detected.")
    else:
        reasons.append(
            f"{conflict_count} potential conflict(s) were detected."
        )

    return {
        "score": round(score, 2),
        "level": level,
        "reasons": reasons,
    }