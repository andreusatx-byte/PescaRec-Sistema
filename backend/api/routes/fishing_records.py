from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from backend.database import get_db
from backend.services.fishing_records_service import FishingRecordsService
from backend.schemas.fishing_record import FishingRecordSchema, FishingRecordCreateSchema

router = APIRouter(
    prefix="/registros",
    tags=["Registros de Pesca"],
    responses={404: {"description": "Registro não encontrado"}},
)

@router.get("/", response_model=List[FishingRecordSchema])
def list_records(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Listar todos os registros de pesca"""
    return FishingRecordsService.get_all_records(db, skip=skip, limit=limit)

@router.get("/ponto/{spot_id}", response_model=List[FishingRecordSchema])
def get_records_by_spot(
    spot_id: int,
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Obter registros de um ponto específico"""
    records = FishingRecordsService.get_records_by_spot(db, spot_id, limit=limit)
    if not records:
        raise HTTPException(status_code=404, detail="Nenhum registro encontrado para este ponto")
    return records

@router.get("/pescador/{fisher_id}", response_model=List[FishingRecordSchema])
def get_records_by_fisher(
    fisher_id: int,
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Obter registros de um pescador específico"""
    records = FishingRecordsService.get_records_by_fisher(db, fisher_id, limit=limit)
    if not records:
        raise HTTPException(status_code=404, detail="Nenhum registro encontrado para este pescador")
    return records

@router.get("/{record_id}", response_model=FishingRecordSchema)
def get_record(
    record_id: int,
    db: Session = Depends(get_db)
):
    """Obter detalhes de um registro de pesca"""
    db_record = FishingRecordsService.get_record_by_id(db, record_id)
    if not db_record:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    return db_record

@router.get("/taxa-sucesso/{spot_id}")
def get_success_rate(
    spot_id: int,
    db: Session = Depends(get_db)
):
    """Obter taxa de sucesso de um ponto"""
    success_rate = FishingRecordsService.calculate_success_rate(db, spot_id)
    return {"spot_id": spot_id, "success_rate": success_rate, "percentage": f"{success_rate * 100:.1f}%"}

@router.post("/", response_model=FishingRecordSchema, status_code=201)
def create_record(
    record_data: FishingRecordCreateSchema,
    db: Session = Depends(get_db)
):
    """Criar novo registro de pesca"""
    return FishingRecordsService.create_record(db, record_data)

@router.put("/{record_id}", response_model=FishingRecordSchema)
def update_record(
    record_id: int,
    record_data: FishingRecordCreateSchema,
    db: Session = Depends(get_db)
):
    """Atualizar um registro de pesca"""
    db_record = FishingRecordsService.update_record(db, record_id, record_data.dict(exclude_unset=True))
    if not db_record:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    return db_record

@router.delete("/{record_id}", status_code=204)
def delete_record(
    record_id: int,
    db: Session = Depends(get_db)
):
    """Deletar um registro de pesca"""
    if not FishingRecordsService.delete_record(db, record_id):
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    return None
