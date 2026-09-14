from sqlalchemy import Column, Integer, Float, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import BaseModel

class Catch(BaseModel):
    __tablename__ = "catches"
    
    record_id = Column(Integer, ForeignKey("fishing_record.id"), nullable=False, index=True)
    species_id = Column(Integer, ForeignKey("species.id"), nullable=False, index=True)
    
    # Medidas
    weight_kg = Column(Float, nullable=True)
    length_cm = Column(Integer, nullable=True)
    
    # Hora da captura
    captured_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Observações
    notes = Column(Text, nullable=True)
    is_released = Column(String(50), default="não")  # 'sim', 'não'
    
    # Relationships
    fishing_record = relationship("FishingRecord", back_populates="catches")
    species = relationship("Species")
    
    def __repr__(self):
        return f"<Catch(id={self.id}, species_id={self.species_id}, weight={self.weight_kg}kg)>"
