from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from typing import List, Optional, Tuple
from datetime import datetime
from backend.models.fishing_spot import FishingSpot
from backend.schemas.fishing_spot import FishingSpotCreateSchema
from math import radians, sin, cos, sqrt, atan2

class FishingSpotsService:
    """Serviço para gerenciar pontos de pesca"""
    
    EARTH_RADIUS_KM = 6371  # Raio da Terra em km
    
    @staticmethod
    def create_spot(db: Session, spot_data: FishingSpotCreateSchema) -> FishingSpot:
        """Criar novo ponto de pesca"""
        db_spot = FishingSpot(**spot_data.dict())
        db.add(db_spot)
        db.commit()
        db.refresh(db_spot)
        return db_spot
    
    @staticmethod
    def get_all_spots(db: Session, skip: int = 0, limit: int = 100) -> List[FishingSpot]:
        """Obter todos os pontos de pesca"""
        return db.query(FishingSpot).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_spot_by_id(db: Session, spot_id: int) -> Optional[FishingSpot]:
        """Obter ponto de pesca por ID"""
        return db.query(FishingSpot).filter(FishingSpot.id == spot_id).first()
    
    @staticmethod
    def get_spots_by_name(db: Session, name: str) -> List[FishingSpot]:
        """Buscar pontos por nome"""
        return db.query(FishingSpot).filter(
            FishingSpot.name.ilike(f"%{name}%")
        ).all()
    
    @staticmethod
    def get_spots_by_access_type(db: Session, access_type: str) -> List[FishingSpot]:
        """Obter pontos por tipo de acesso"""
        return db.query(FishingSpot).filter(
            FishingSpot.access_type.ilike(access_type)
        ).all()
    
    @staticmethod
    def get_spots_by_radius(db: Session, latitude: float, longitude: float, radius_km: float) -> List[FishingSpot]:
        """Obter pontos dentro de um raio (em km)
        
        Usa cálculo de distância Haversine
        """
        spots = db.query(FishingSpot).all()
        nearby_spots = []
        
        for spot in spots:
            distance = FishingSpotsService._haversine_distance(
                latitude, longitude,
                float(spot.latitude), float(spot.longitude)
            )
            if distance <= radius_km:
                nearby_spots.append(spot)
        
        return sorted(nearby_spots, key=lambda x: FishingSpotsService._haversine_distance(
            latitude, longitude,
            float(x.latitude), float(x.longitude)
        ))
    
    @staticmethod
    def get_best_rated_spots(db: Session, limit: int = 10) -> List[FishingSpot]:
        """Obter pontos mais bem avaliados"""
        return db.query(FishingSpot).order_by(
            desc(FishingSpot.average_rating),
            desc(FishingSpot.success_rate)
        ).limit(limit).all()
    
    @staticmethod
    def get_most_visited_spots(db: Session, limit: int = 10) -> List[FishingSpot]:
        """Obter pontos mais visitados"""
        return db.query(FishingSpot).order_by(
            desc(FishingSpot.visits_count)
        ).limit(limit).all()
    
    @staticmethod
    def update_spot(db: Session, spot_id: int, spot_data: dict) -> Optional[FishingSpot]:
        """Atualizar ponto de pesca"""
        db_spot = db.query(FishingSpot).filter(FishingSpot.id == spot_id).first()
        if db_spot:
            for key, value in spot_data.items():
                if value is not None:
                    setattr(db_spot, key, value)
            db_spot.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(db_spot)
        return db_spot
    
    @staticmethod
    def update_spot_rating(db: Session, spot_id: int, new_rating: float) -> Optional[FishingSpot]:
        """Atualizar avaliação do ponto"""
        db_spot = db.query(FishingSpot).filter(FishingSpot.id == spot_id).first()
        if db_spot:
            # Média ponderada com avaliação anterior
            total_ratings = db_spot.visits_count
            old_total = db_spot.average_rating * total_ratings
            db_spot.average_rating = (old_total + new_rating) / (total_ratings + 1)
            db.commit()
            db.refresh(db_spot)
        return db_spot
    
    @staticmethod
    def increment_visit_count(db: Session, spot_id: int) -> Optional[FishingSpot]:
        """Incrementar contagem de visitas"""
        db_spot = db.query(FishingSpot).filter(FishingSpot.id == spot_id).first()
        if db_spot:
            db_spot.visits_count += 1
            db.commit()
            db.refresh(db_spot)
        return db_spot
    
    @staticmethod
    def update_success_rate(db: Session, spot_id: int, success_rate: float) -> Optional[FishingSpot]:
        """Atualizar taxa de sucesso"""
        db_spot = db.query(FishingSpot).filter(FishingSpot.id == spot_id).first()
        if db_spot:
            db_spot.success_rate = max(0.0, min(1.0, success_rate))  # Limitar entre 0 e 1
            db.commit()
            db.refresh(db_spot)
        return db_spot
    
    @staticmethod
    def delete_spot(db: Session, spot_id: int) -> bool:
        """Deletar ponto de pesca"""
        db_spot = db.query(FishingSpot).filter(FishingSpot.id == spot_id).first()
        if db_spot:
            db.delete(db_spot)
            db.commit()
            return True
        return False
    
    @staticmethod
    def _haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calcular distância entre dois pontos geográficos usando fórmula Haversine"""
        lat1_rad = radians(lat1)
        lon1_rad = radians(lon1)
        lat2_rad = radians(lat2)
        lon2_rad = radians(lon2)
        
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        
        return FishingSpotsService.EARTH_RADIUS_KM * c
