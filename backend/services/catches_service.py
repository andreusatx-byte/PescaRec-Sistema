from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from backend.models.catch import Catch
from backend.schemas.catch import CatchCreateSchema

class CatchesService:
    """Serviço para gerenciar capturas de peixes"""
    
    @staticmethod
    def create_catch(db: Session, catch_data: CatchCreateSchema) -> Catch:
        """Criar novo registro de captura"""
        db_catch = Catch(**catch_data.dict())
        if not db_catch.captured_at:
            db_catch.captured_at = datetime.utcnow()
        db.add(db_catch)
        db.commit()
        db.refresh(db_catch)
        return db_catch
    
    @staticmethod
    def get_catch_by_id(db: Session, catch_id: int) -> Optional[Catch]:
        """Obter captura por ID"""
        return db.query(Catch).filter(Catch.id == catch_id).first()
    
    @staticmethod
    def get_catches_by_record(db: Session, record_id: int) -> List[Catch]:
        """Obter todas as capturas de um registro"""
        return db.query(Catch).filter(Catch.record_id == record_id).all()
    
    @staticmethod
    def get_catches_by_species(db: Session, species_id: int, limit: int = 100) -> List[Catch]:
        """Obter capturas de uma espécie específica"""
        return db.query(Catch).filter(
            Catch.species_id == species_id
        ).limit(limit).all()
    
    @staticmethod
    def get_average_weight_by_species(db: Session, species_id: int) -> float:
        """Calcular peso médio de uma espécie"""
        catches = db.query(Catch).filter(
            Catch.species_id == species_id
        ).all()
        
        if not catches:
            return 0.0
        
        valid_catches = [c for c in catches if c.weight_kg and c.weight_kg > 0]
        if not valid_catches:
            return 0.0
        
        return sum(c.weight_kg for c in valid_catches) / len(valid_catches)
    
    @staticmethod
    def get_average_length_by_species(db: Session, species_id: int) -> float:
        """Calcular tamanho médio de uma espécie"""
        catches = db.query(Catch).filter(
            Catch.species_id == species_id
        ).all()
        
        if not catches:
            return 0.0
        
        valid_catches = [c for c in catches if c.length_cm and c.length_cm > 0]
        if not valid_catches:
            return 0.0
        
        return sum(c.length_cm for c in valid_catches) / len(valid_catches)
    
    @staticmethod
    def update_catch(db: Session, catch_id: int, catch_data: dict) -> Optional[Catch]:
        """Atualizar captura"""
        db_catch = db.query(Catch).filter(Catch.id == catch_id).first()
        if db_catch:
            for key, value in catch_data.items():
                if value is not None:
                    setattr(db_catch, key, value)
            db_catch.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(db_catch)
        return db_catch
    
    @staticmethod
    def delete_catch(db: Session, catch_id: int) -> bool:
        """Deletar captura"""
        db_catch = db.query(Catch).filter(Catch.id == catch_id).first()
        if db_catch:
            db.delete(db_catch)
            db.commit()
            return True
        return False
