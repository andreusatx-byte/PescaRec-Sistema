from sqlalchemy.orm import Session
from typing import List, Optional
from backend.models.species import Species
from backend.schemas.species import SpeciesCreateSchema

class SpeciesService:
    """Serviço para gerenciar espécies de peixes"""
    
    @staticmethod
    def create_species(db: Session, species_data: SpeciesCreateSchema) -> Species:
        """Criar nova espécie"""
        db_species = Species(**species_data.dict())
        db.add(db_species)
        db.commit()
        db.refresh(db_species)
        return db_species
    
    @staticmethod
    def get_all_species(db: Session, skip: int = 0, limit: int = 100) -> List[Species]:
        """Obter todas as espécies com paginação"""
        return db.query(Species).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_species_by_id(db: Session, species_id: int) -> Optional[Species]:
        """Obter espécie por ID"""
        return db.query(Species).filter(Species.id == species_id).first()
    
    @staticmethod
    def get_species_by_name(db: Session, common_name: str) -> Optional[Species]:
        """Obter espécie por nome comum"""
        return db.query(Species).filter(
            Species.common_name.ilike(f"%{common_name}%")
        ).first()
    
    @staticmethod
    def search_species(db: Session, search_term: str) -> List[Species]:
        """Buscar espécies por termo"""
        return db.query(Species).filter(
            Species.common_name.ilike(f"%{search_term}%") |
            Species.scientific_name.ilike(f"%{search_term}%")
        ).all()
    
    @staticmethod
    def get_species_by_season(db: Session, season: str) -> List[Species]:
        """Obter espécies por estação"""
        return db.query(Species).filter(
            Species.best_season.ilike(f"%{season}%")
        ).all()
    
    @staticmethod
    def get_species_by_habitat(db: Session, habitat: str) -> List[Species]:
        """Obter espécies por habitat"""
        return db.query(Species).filter(
            Species.habitat.ilike(f"%{habitat}%")
        ).all()
    
    @staticmethod
    def update_species(db: Session, species_id: int, species_data: dict) -> Optional[Species]:
        """Atualizar espécie"""
        db_species = db.query(Species).filter(Species.id == species_id).first()
        if db_species:
            for key, value in species_data.items():
                if value is not None:
                    setattr(db_species, key, value)
            db.commit()
            db.refresh(db_species)
        return db_species
    
    @staticmethod
    def delete_species(db: Session, species_id: int) -> bool:
        """Deletar espécie"""
        db_species = db.query(Species).filter(Species.id == species_id).first()
        if db_species:
            db.delete(db_species)
            db.commit()
            return True
        return False
