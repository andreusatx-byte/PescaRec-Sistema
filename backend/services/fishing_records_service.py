from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from typing import List, Optional
from datetime import date, datetime
from backend.models.fishing_record import FishingRecord
from backend.schemas.fishing_record import FishingRecordCreateSchema

class FishingRecordsService:
    """Serviço para gerenciar registros de pesca"""
    
    @staticmethod
    def create_record(db: Session, record_data: FishingRecordCreateSchema) -> FishingRecord:
        """Criar novo registro de pesca"""
        db_record = FishingRecord(**record_data.dict())
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        return db_record
    
    @staticmethod
    def get_all_records(db: Session, skip: int = 0, limit: int = 100) -> List[FishingRecord]:
        """Obter todos os registros de pesca"""
        return db.query(FishingRecord).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_record_by_id(db: Session, record_id: int) -> Optional[FishingRecord]:
        """Obter registro por ID"""
        return db.query(FishingRecord).filter(FishingRecord.id == record_id).first()
    
    @staticmethod
    def get_records_by_spot(db: Session, spot_id: int, limit: int = 100) -> List[FishingRecord]:
        """Obter registros de um ponto de pesca específico"""
        return db.query(FishingRecord).filter(
            FishingRecord.spot_id == spot_id
        ).order_by(desc(FishingRecord.fishing_date)).limit(limit).all()
    
    @staticmethod
    def get_records_by_fisher(db: Session, fisher_id: int, limit: int = 100) -> List[FishingRecord]:
        """Obter registros de um pescador específico"""
        return db.query(FishingRecord).filter(
            FishingRecord.fisher_id == fisher_id
        ).order_by(desc(FishingRecord.fishing_date)).limit(limit).all()
    
    @staticmethod
    def get_records_by_date_range(db: Session, start_date: date, end_date: date) -> List[FishingRecord]:
        """Obter registros em um período"""
        return db.query(FishingRecord).filter(
            and_(
                FishingRecord.fishing_date >= start_date,
                FishingRecord.fishing_date <= end_date
            )
        ).order_by(desc(FishingRecord.fishing_date)).all()
    
    @staticmethod
    def get_records_by_tide_phase(db: Session, tide_phase: str) -> List[FishingRecord]:
        """Obter registros de uma fase de maré específica"""
        return db.query(FishingRecord).filter(
            FishingRecord.tide_phase.ilike(tide_phase)
        ).all()
    
    @staticmethod
    def calculate_success_rate(db: Session, spot_id: int) -> float:
        """Calcular taxa de sucesso de um ponto
        
        Taxa de sucesso = registros com capturas / total de registros
        """
        total_records = db.query(FishingRecord).filter(
            FishingRecord.spot_id == spot_id
        ).count()
        
        if total_records == 0:
            return 0.0
        
        successful_records = db.query(FishingRecord).filter(
            and_(
                FishingRecord.spot_id == spot_id,
                FishingRecord.total_catches > 0
            )
        ).count()
        
        return successful_records / total_records
    
    @staticmethod
    def get_best_fishing_period(db: Session, spot_id: int) -> Optional[str]:
        """Obter melhor período de pesca (maré) para um ponto"""
        records = db.query(FishingRecord).filter(
            and_(
                FishingRecord.spot_id == spot_id,
                FishingRecord.total_catches > 0
            )
        ).all()
        
        if not records:
            return None
        
        tide_phases = {}
        for record in records:
            if record.tide_phase:
                if record.tide_phase not in tide_phases:
                    tide_phases[record.tide_phase] = 0
                tide_phases[record.tide_phase] += record.total_catches
        
        return max(tide_phases, key=tide_phases.get) if tide_phases else None
    
    @staticmethod
    def get_average_catch_weight(db: Session, spot_id: int) -> float:
        """Obter peso médio de capturas em um ponto"""
        records = db.query(FishingRecord).filter(
            FishingRecord.spot_id == spot_id
        ).all()
        
        if not records:
            return 0.0
        
        total_weight = sum(record.total_weight_kg for record in records if record.total_weight_kg)
        record_count = len([r for r in records if r.total_weight_kg and r.total_weight_kg > 0])
        
        return total_weight / record_count if record_count > 0 else 0.0
    
    @staticmethod
    def update_record(db: Session, record_id: int, record_data: dict) -> Optional[FishingRecord]:
        """Atualizar registro de pesca"""
        db_record = db.query(FishingRecord).filter(FishingRecord.id == record_id).first()
        if db_record:
            for key, value in record_data.items():
                if value is not None:
                    setattr(db_record, key, value)
            db_record.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(db_record)
        return db_record
    
    @staticmethod
    def delete_record(db: Session, record_id: int) -> bool:
        """Deletar registro de pesca"""
        db_record = db.query(FishingRecord).filter(FishingRecord.id == record_id).first()
        if db_record:
            db.delete(db_record)
            db.commit()
            return True
        return False
