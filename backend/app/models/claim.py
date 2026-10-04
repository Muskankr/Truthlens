from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Claim(Base):
    __tablename__ = "claims"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    chunk_id: Mapped[int] = mapped_column(
        ForeignKey("document_chunks.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    claim_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    claim_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="general",
    )

    confidence: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    # ---------------------------------------------------------
    # Temporal / version-aware reasoning
    # ---------------------------------------------------------

    effective_date: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    version: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    chunk = relationship(
        "DocumentChunk",
        back_populates="claims",
    )

    evidence = relationship(
        "Evidence",
        back_populates="claim",
        cascade="all, delete-orphan",
    )