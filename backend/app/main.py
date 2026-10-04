from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router
from app.api.db_test import router as db_test_router
from app.api.documents import router as documents_router
from app.api.search import router as search_router
from app.api.evidence import router as evidence_router
from app.api.claims import router as claims_router
from app.api.conflicts import router as conflicts_router
from app.api.confidence import router as confidence_router
from app.api.investigations import router as investigations_router


app = FastAPI(
    title="TruthLens API",
    description="Evidence-aware AI document investigation platform",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(health_router, prefix="/api")
app.include_router(db_test_router, prefix="/api")
app.include_router(documents_router, prefix="/api/documents")
app.include_router(search_router, prefix="/api")
app.include_router(evidence_router, prefix="/api")
app.include_router(claims_router, prefix="/api")
app.include_router(conflicts_router, prefix="/api")
app.include_router(confidence_router, prefix="/api")
app.include_router(investigations_router, prefix="/api")


@app.get("/")
def root():
    return {
        "message": "TruthLens API is running",
        "version": "0.1.0"
    }