from .species import router as species_router
from .fishing_spots import router as fishing_spots_router
from .fishing_records import router as fishing_records_router
from .catches import router as catches_router

__all__ = [
    "species_router",
    "fishing_spots_router",
    "fishing_records_router",
    "catches_router",
]
