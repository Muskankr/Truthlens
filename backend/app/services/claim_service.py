import re
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.claim import Claim
from app.models.chunk import DocumentChunk


PERCENTAGE_PATTERN = re.compile(
    r"\b\d+(?:\.\d+)?\s*%"
)

MONEY_PATTERN = re.compile(
    r"(?:₹|\$|€|£)\s?\d+(?:,\d{3})*(?:\.\d+)?"
)

DATE_PATTERN = re.compile(
    r"\b(?:"
    r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}"
    r"|"
    r"\d{1,2}\s+"
    r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
    r"(?:uary|ruary|ch|il|y|ust|tember|ober|vember|cember)?"
    r"(?:\s+\d{4})?"
    r"|"
    r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
    r"(?:uary|ruary|ch|il|y|ust|tember|ober|vember|cember)?"
    r"\s+\d{1,2},?\s+\d{4}"
    r"|"
    r"\d{4}-\d{1,2}-\d{1,2}"
    r")\b",
    re.IGNORECASE,
)

VERSION_PATTERN = re.compile(
    r"\b(?:version|ver\.?|v)\s*[-:]?\s*(\d+(?:\.\d+)*)\b",
    re.IGNORECASE,
)


def classify_claim(text: str) -> str:
    """
    Assign a simple claim type based on detectable patterns.
    """

    if PERCENTAGE_PATTERN.search(text):
        return "percentage"

    if MONEY_PATTERN.search(text):
        return "financial"

    if DATE_PATTERN.search(text):
        return "date"

    lowered = text.lower()

    if any(
        word in lowered
        for word in [
            "must",
            "shall",
            "required",
            "mandatory",
        ]
    ):
        return "requirement"

    if any(
        word in lowered
        for word in [
            "may",
            "can",
            "allowed",
            "permitted",
        ]
    ):
        return "permission"

    return "general"


def parse_date(text: str) -> datetime | None:
    """
    Extract the first recognizable date from text.

    Supported examples:
    - 01/06/2026
    - 01-06-2026
    - 2026-06-01
    - 1 June 2026
    - June 1, 2026
    """

    match = DATE_PATTERN.search(text)

    if not match:
        return None

    value = match.group(0).strip()

    formats = [
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%d/%m/%y",
        "%d-%m-%y",
        "%Y-%m-%d",
        "%d %B %Y",
        "%d %b %Y",
        "%B %d, %Y",
        "%B %d %Y",
        "%b %d, %Y",
        "%b %d %Y",
        "%d %B",
        "%d %b",
    ]

    for date_format in formats:
        try:
            parsed = datetime.strptime(
                value,
                date_format,
            )

            # If the source contains only day + month,
            # use the current year.
            if "%Y" not in date_format:
                parsed = parsed.replace(
                    year=datetime.utcnow().year
                )

            return parsed

        except ValueError:
            continue

    return None


def extract_version(text: str) -> str | None:
    """
    Extract an explicit document/claim version.

    Examples:
    - Version 2
    - version 2.1
    - v2
    - v2.1
    - Ver. 3
    """

    match = VERSION_PATTERN.search(text)

    if not match:
        return None

    return match.group(1)


def extract_claims_from_text(text: str) -> list[dict]:
    """
    Extract sentence-level claims together with
    temporal/version metadata.

    This is the deterministic claim extraction layer.
    """

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text.strip(),
    )

    claims = []

    for sentence in sentences:

        sentence = sentence.strip()

        if len(sentence) < 15:
            continue

        claim_date = parse_date(sentence)
        version = extract_version(sentence)

        claims.append(
            {
                "claim_text": sentence,
                "claim_type": classify_claim(sentence),
                "effective_date": claim_date,
                "version": version,
            }
        )

    return claims


def extract_claims_for_chunk(
    db: Session,
    chunk: DocumentChunk,
) -> list[Claim]:

    extracted_claims = extract_claims_from_text(
        chunk.content
    )

    claims = []

    for item in extracted_claims:

        claim = Claim(
            document_id=chunk.document_id,
            chunk_id=chunk.id,
            claim_text=item["claim_text"],
            claim_type=item["claim_type"],
            confidence=0.70,
            effective_date=item["effective_date"],
            version=item["version"],
        )

        db.add(claim)
        claims.append(claim)

    return claims