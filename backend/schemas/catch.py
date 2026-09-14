from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CatchSchema(BaseModel):
    id: int
    record_id: int
    species_id: int
    weight_kg: Optional[float] = None
    length_cm: Optional[int] = None
    captured_at: datetime
    notes: Optional[str] = None
    is_released: str = "não"
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class CatchCreateSchema(BaseModel):
    record_id: int = Field(..., gt=0)
    species_id: int = Field(..., gt=0)
    weight_kg: Optional[float] = Field(None, gt=0)
    length_cm: Optional[int] = Field(None, gt=0)
    captured_at: Optional[datetime] = None
    notes: Optional[str] = None
    is_released: str = Field("não", regex="^(sim|não)$")
