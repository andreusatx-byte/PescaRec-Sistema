from fastapi import APIRouter
from .routes import (
    species_router,
    fishing_spots_router,
    fishing_records_router,
    catches_router,
)

router = APIRouter(prefix="/api")

router.include_router(species_router)
router.include_router(fishing_spots_router)
router.include_router(fishing_records_router)
router.include_router(catches_router)

__all__ = ["router"]
