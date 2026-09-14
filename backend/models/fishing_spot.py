from sqlalchemy import Column, String, Float, Integer, Text, Numeric
from sqlalchemy.orm import relationship
from .base import BaseModel

class FishingSpot(BaseModel):
    __tablename__ = "fishing_spots"
    
    name = Column(String(255), nullable=False, index=True)
    latitude = Column(Numeric(10, 8), nullable=False)
    longitude = Column(Numeric(11, 8), nullable=False)
    description = Column(Text, nullable=True)
    
    # Tipo de acesso
    access_type = Column(String(50), nullable=False)  # 'barco', 'praia', 'cais'
    
    # Características geográficas
    depth_avg = Column(Integer, nullable=True)  # em metros
    bottom_type = Column(String(100), nullable=True)  # 'areia', 'rocha', 'lama', etc.
    
    # Avaliação
    average_rating = Column(Float, default=0.0)
    visits_count = Column(Integer, default=0)
    success_rate = Column(Float, default=0.0)  # 0 a 1 (0% a 100%)
    
    # Observações
    notes = Column(Text, nullable=True)
    
    # Relationships
    fishing_records = relationship("FishingRecord", back_populates="fishing_spot")
    species = relationship("Species", secondary="species_locations", backref="fishing_spots")
    
    def __repr__(self):
        return f"<FishingSpot(id={self.id}, name='{self.name}', lat={self.latitude}, lon={self.longitude})>"
