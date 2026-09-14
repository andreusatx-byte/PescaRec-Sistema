from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class FishingSpotSchema(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    description: Optional[str] = None
    access_type: str
    depth_avg: Optional[int] = None
    bottom_type: Optional[str] = None
    average_rating: float = 0.0
    visits_count: int = 0
    success_rate: float = 0.0
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class FishingSpotCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    description: Optional[str] = None
    access_type: str = Field(..., min_length=1)
    depth_avg: Optional[int] = None
    bottom_type: Optional[str] = None
    notes: Optional[str] = None
