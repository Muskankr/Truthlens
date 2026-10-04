from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.claim import Claim
from app.models.chunk import DocumentChunk
from app.services.claim_service import (
    extract_claims_from_text,
    parse_date,
    extract_version,
)


router = APIRouter()


@router.post("/claims/extract")
def extract_document_claims(
    db: Session = Depends(get_db),
):
    """
    Extract claims from document chunks.

    Temporal/version metadata is propagated through each
    document so claims can inherit metadata stated in
    preceding sections or chunks.

    Existing claims are also backfilled with temporal
    metadata when it is available.
    """

    documents = db.execute(
        select(DocumentChunk.document_id)
        .distinct()
        .order_by(DocumentChunk.document_id)
    ).scalars().all()

    created_claims = []
    updated_claims = []

    for document_id in documents:

        chunks = db.execute(
            select(DocumentChunk)
            .where(
                DocumentChunk.document_id == document_id
            )
            .order_by(DocumentChunk.chunk_index)
        ).scalars().all()

        current_effective_date = None
        current_version = None

        for chunk in chunks:

            # -------------------------------------------------
            # 1. Detect temporal/version metadata FIRST
            # -------------------------------------------------

            chunk_date = parse_date(
                chunk.content
            )

            chunk_version = extract_version(
                chunk.content
            )

            if chunk_date is not None:
                current_effective_date = chunk_date

            if chunk_version is not None:
                current_version = chunk_version

            # -------------------------------------------------
            # 2. Check existing claims
            # -------------------------------------------------

            existing_claims = db.execute(
                select(Claim)
                .where(
                    Claim.chunk_id == chunk.id
                )
            ).scalars().all()

            if existing_claims:

                # Backfill missing temporal metadata.
                for claim in existing_claims:

                    changed = False

                    if (
                        claim.effective_date is None
                        and current_effective_date is not None
                    ):
                        claim.effective_date = (
                            current_effective_date
                        )
                        changed = True

                    if (
                        claim.version is None
                        and current_version is not None
                    ):
                        claim.version = current_version
                        changed = True

                    if changed:
                        updated_claims.append(
                            claim.id
                        )

                # Do not create duplicate claims.
                continue

            # -------------------------------------------------
            # 3. Extract new claims
            # -------------------------------------------------

            extracted_claims = (
                extract_claims_from_text(
                    chunk.content
                )
            )

            for item in extracted_claims:

                claim_date = (
                    item["effective_date"]
                    or current_effective_date
                )

                claim_version = (
                    item["version"]
                    or current_version
                )

                claim = Claim(
                    document_id=chunk.document_id,
                    chunk_id=chunk.id,
                    claim_text=item["claim_text"],
                    claim_type=item["claim_type"],
                    confidence=0.70,
                    effective_date=claim_date,
                    version=claim_version,
                )

                db.add(claim)
                created_claims.append(claim)

    db.commit()

    return {
        "status": "success",
        "claims_created": len(created_claims),
        "claims_updated": len(updated_claims),
    }


@router.get("/claims")
def list_claims(
    db: Session = Depends(get_db),
):
    claims = db.execute(
        select(Claim).order_by(Claim.id)
    ).scalars().all()

    return {
        "count": len(claims),
        "claims": [
            {
                "id": claim.id,
                "document_id": claim.document_id,
                "chunk_id": claim.chunk_id,
                "claim_text": claim.claim_text,
                "claim_type": claim.claim_type,
                "confidence": claim.confidence,
                "effective_date": (
                    claim.effective_date.isoformat()
                    if claim.effective_date
                    else None
                ),
                "version": claim.version,
            }
            for claim in claims
        ],
    }