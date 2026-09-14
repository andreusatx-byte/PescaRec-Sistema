from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class SpeciesSchema(BaseModel):
    id: int
    common_name: str
    scientific_name: Optional[str] = None
    family: Optional[str] = None
    description: Optional[str] = None
    average_weight_kg: Optional[float] = None
    max_weight_kg: Optional[float] = None
    average_length_cm: Optional[int] = None
    max_length_cm: Optional[int] = None
    habitat: Optional[str] = None
    best_season: Optional[str] = None
    best_tide_phase: Optional[str] = None
    best_hours: Optional[str] = None
    depth_range: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class SpeciesCreateSchema(BaseModel):
    common_name: str = Field(..., min_length=1, max_length=255)
    scientific_name: Optional[str] = None
    family: Optional[str] = None
    description: Optional[str] = None
    average_weight_kg: Optional[float] = None
    max_weight_kg: Optional[float] = None
    average_length_cm: Optional[int] = None
    max_length_cm: Optional[int] = None
    habitat: Optional[str] = None
    best_season: Optional[str] = None
    best_tide_phase: Optional[str] = None
    best_hours: Optional[str] = None
    depth_range: Optional[str] = None
