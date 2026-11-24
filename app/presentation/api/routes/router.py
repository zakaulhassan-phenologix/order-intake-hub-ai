from fastapi import APIRouter

from app.presentation.api.routes import (
    classification,
    confidence,
    extraction,
    health,
    learning,
    matching,
    shadow_mode,
)

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(classification.router, prefix="/classify", tags=["classification"])
api_router.include_router(extraction.router, prefix="/extract", tags=["extraction"])
api_router.include_router(matching.router, prefix="/match-products", tags=["matching"])
api_router.include_router(confidence.router, prefix="/confidence", tags=["confidence"])
api_router.include_router(learning.router, prefix="/learning", tags=["learning"])
api_router.include_router(shadow_mode.router, prefix="/shadow-mode", tags=["shadow-mode"])
