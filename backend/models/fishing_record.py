from sqlalchemy import Column, String, Integer, Text, Date, Time, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import BaseModel

class FishingRecord(BaseModel):
    __tablename__ = "fishing_records"
    
    spot_id = Column(Integer, ForeignKey("fishing_spot.id"), nullable=False, index=True)
    fisher_id = Column(Integer, nullable=True)  # Referência ao usuário (para versão com auth)
    
    # Data e hora
    fishing_date = Column(Date, nullable=False, index=True)
    start_time = Column(Time, nullable=True)
    end_time = Column(Time, nullable=True)
    
    # Condições de maré e clima
    tide_level = Column(String(50), nullable=True)  # 'alta', 'média', 'baixa'
    tide_phase = Column(String(50), nullable=True)  # 'enchente', vazante'
    moon_phase = Column(String(50), nullable=True)  # 'nova', 'crescente', 'cheia', 'minguante'
    weather_condition = Column(String(100), nullable=True)
    water_temperature_c = Column(Float, nullable=True)
    wind_speed_kmh = Column(Float, nullable=True)
    
    # Resultados
    total_catches = Column(Integer, default=0)
    total_weight_kg = Column(Float, default=0.0)
    
    # Observações
    notes = Column(Text, nullable=True)
    
    # Relationships
    fishing_spot = relationship("FishingSpot", back_populates="fishing_records")
    catches = relationship("Catch", back_populates="fishing_record", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<FishingRecord(id={self.id}, spot_id={self.spot_id}, date={self.fishing_date})>"
