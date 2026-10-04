from app.db.base import Base
from app.db.session import engine
from app.models import (
    Document,
    DocumentChunk,
    Claim,
    Investigation,
    Evidence,
)


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("TruthLens database tables created successfully.")