import re

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.claim import Claim


PERCENTAGE_PATTERN = re.compile(
    r"(\d+(?:\.\d+)?)\s*%"
)

MONEY_PATTERN = re.compile(
    r"(?:₹|\$|€|£)\s?(\d+(?:,\d{3})*(?:\.\d+)?)"
)


def extract_value(
    claim_text: str,
    claim_type: str,
):
    if claim_type == "percentage":
        match = PERCENTAGE_PATTERN.search(claim_text)

        if match:
            return float(match.group(1))

    if claim_type == "financial":
        match = MONEY_PATTERN.search(claim_text)

        if match:
            return float(
                match.group(1).replace(",", "")
            )

    return None


def get_claim_keywords(
    text: str,
) -> set[str]:
    """
    Extract meaningful keywords from a claim.
    """

    stop_words = {
        "the",
        "and",
        "for",
        "with",
        "that",
        "this",
        "shall",
        "must",
        "will",
        "are",
        "was",
        "were",
        "from",
        "into",
        "than",
        "then",
        "their",
        "they",
        "have",
        "has",
        "been",
        "can",
        "may",
    }

    words = re.findall(
        r"\b[a-zA-Z0-9]+\b",
        text.lower(),
    )

    return {
        word
        for word in words
        if len(word) >= 3
        and word not in stop_words
    }


def claims_are_related(
    claim_a: Claim,
    claim_b: Claim,
    minimum_overlap: int = 2,
) -> bool:
    """
    Determine whether two claims are about a similar subject.

    This prevents unrelated percentages or financial values
    from being treated as conflicts.
    """

    keywords_a = get_claim_keywords(
        claim_a.claim_text
    )

    keywords_b = get_claim_keywords(
        claim_b.claim_text
    )

    overlap = keywords_a.intersection(
        keywords_b
    )

    return len(overlap) >= minimum_overlap


def parse_version(
    version: str | None,
) -> float | None:
    """
    Convert a version string into a comparable number.

    Examples:
        "1"   -> 1.0
        "2"   -> 2.0
        "2.1" -> 2.1
    """

    if not version:
        return None

    try:
        return float(version)
    except (TypeError, ValueError):
        return None


def determine_temporal_relationship(
    claim_a: Claim,
    claim_b: Claim,
) -> tuple[str, str]:
    """
    Determine whether two different claims represent:

    - a newer version superseding an older one
    - a newer effective date superseding an older one
    - an unresolved potential conflict

    Returns:
        (status, relationship)
    """

    version_a = parse_version(
        claim_a.version
    )

    version_b = parse_version(
        claim_b.version
    )

    # ---------------------------------------------------------
    # Version-based precedence
    # ---------------------------------------------------------

    if (
        version_a is not None
        and version_b is not None
        and version_a != version_b
    ):
        if version_a > version_b:
            return (
                "superseded",
                "claim_a_newer_version",
            )

        return (
            "superseded",
            "claim_b_newer_version",
        )

    # ---------------------------------------------------------
    # Effective-date precedence
    # ---------------------------------------------------------

    if (
        claim_a.effective_date is not None
        and claim_b.effective_date is not None
        and claim_a.effective_date
        != claim_b.effective_date
    ):
        if (
            claim_a.effective_date
            > claim_b.effective_date
        ):
            return (
                "superseded",
                "claim_a_newer_effective_date",
            )

        return (
            "superseded",
            "claim_b_newer_effective_date",
        )

    # ---------------------------------------------------------
    # Same temporal information
    # ---------------------------------------------------------

    if (
        version_a is not None
        and version_b is not None
        and version_a == version_b
    ):
        return (
            "potential_conflict",
            "same_version",
        )

    if (
        claim_a.effective_date is not None
        and claim_b.effective_date is not None
        and claim_a.effective_date
        == claim_b.effective_date
    ):
        return (
            "potential_conflict",
            "same_effective_date",
        )

    # ---------------------------------------------------------
    # No temporal information
    # ---------------------------------------------------------

    return (
        "potential_conflict",
        "no_temporal_precedence",
    )


def find_conflicts(
    db: Session,
    relevant_chunk_ids: set[int] | None = None,
) -> list[dict]:
    """
    Find potential conflicts between related claims.

    Temporal/version metadata is used to distinguish an actual
    unresolved conflict from an older claim that may have been
    superseded by a newer claim.
    """

    stmt = select(Claim).order_by(
        Claim.id
    )

    if relevant_chunk_ids:
        stmt = stmt.where(
            Claim.chunk_id.in_(
                relevant_chunk_ids
            )
        )

    claims = (
        db.execute(stmt)
        .scalars()
        .all()
    )

    conflicts = []

    for i in range(len(claims)):

        claim_a = claims[i]

        value_a = extract_value(
            claim_a.claim_text,
            claim_a.claim_type,
        )

        if value_a is None:
            continue

        for j in range(i + 1, len(claims)):

            claim_b = claims[j]

            if (
                claim_a.claim_type
                != claim_b.claim_type
            ):
                continue

            if not claims_are_related(
                claim_a,
                claim_b,
            ):
                continue

            value_b = extract_value(
                claim_b.claim_text,
                claim_b.claim_type,
            )

            if value_b is None:
                continue

            # Same value is not a conflict.
            if value_a == value_b:
                continue

            status, relationship = (
                determine_temporal_relationship(
                    claim_a,
                    claim_b,
                )
            )

            conflicts.append(
                {
                    "claim_a": {
                        "id": claim_a.id,
                        "document_id": claim_a.document_id,
                        "chunk_id": claim_a.chunk_id,
                        "text": claim_a.claim_text,
                        "value": value_a,
                        "effective_date": (
                            claim_a.effective_date.isoformat()
                            if claim_a.effective_date
                            else None
                        ),
                        "version": claim_a.version,
                    },
                    "claim_b": {
                        "id": claim_b.id,
                        "document_id": claim_b.document_id,
                        "chunk_id": claim_b.chunk_id,
                        "text": claim_b.claim_text,
                        "value": value_b,
                        "effective_date": (
                            claim_b.effective_date.isoformat()
                            if claim_b.effective_date
                            else None
                        ),
                        "version": claim_b.version,
                    },
                    "conflict_type": claim_a.claim_type,
                    "status": status,
                    "relationship": relationship,
                }
            )

    return conflicts