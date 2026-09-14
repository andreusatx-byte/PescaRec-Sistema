from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, time, datetime

class FishingRecordSchema(BaseModel):
    id: int
    spot_id: int
    fisher_id: Optional[int] = None
    fishing_date: date
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    tide_level: Optional[str] = None
    tide_phase: Optional[str] = None
    moon_phase: Optional[str] = None
    weather_condition: Optional[str] = None
    water_temperature_c: Optional[float] = None
    wind_speed_kmh: Optional[float] = None
    total_catches: int = 0
    total_weight_kg: float = 0.0
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class FishingRecordCreateSchema(BaseModel):
    spot_id: int = Field(..., gt=0)
    fisher_id: Optional[int] = None
    fishing_date: date
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    tide_level: Optional[str] = None
    tide_phase: Optional[str] = None
    moon_phase: Optional[str] = None
    weather_condition: Optional[str] = None
    water_temperature_c: Optional[float] = None
    wind_speed_kmh: Optional[float] = None
    notes: Optional[str] = None
