from sqlalchemy import Column, String, Float, Integer, Text
from .base import BaseModel

class Species(BaseModel):
    __tablename__ = "species"
    
    common_name = Column(String(255), unique=True, nullable=False, index=True)
    scientific_name = Column(String(255), nullable=True)
    family = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    
    # Tamanhos
    average_weight_kg = Column(Float, nullable=True)
    max_weight_kg = Column(Float, nullable=True)
    average_length_cm = Column(Integer, nullable=True)
    max_length_cm = Column(Integer, nullable=True)
    
    # Características de habitat
    habitat = Column(String(255), nullable=True)
    best_season = Column(String(100), nullable=True)
    best_tide_phase = Column(String(50), nullable=True)  # 'enchente', 'vazante', 'média'
    best_hours = Column(String(50), nullable=True)
    depth_range = Column(String(100), nullable=True)
    
    def __repr__(self):
        return f"<Species(id={self.id}, common_name='{self.common_name}')>"
