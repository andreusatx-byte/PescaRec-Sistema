from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.services.catches_service import CatchesService
from backend.schemas.catch import CatchSchema, CatchCreateSchema

router = APIRouter(
    prefix="/capturas",
    tags=["Capturas de Peixes"],
    responses={404: {"description": "Captura não encontrada"}},
)

@router.get("/registro/{record_id}", response_model=List[CatchSchema])
def get_catches_by_record(
    record_id: int,
    db: Session = Depends(get_db)
):
    """Obter capturas de um registro específico"""
    catches = CatchesService.get_catches_by_record(db, record_id)
    if not catches:
        raise HTTPException(status_code=404, detail="Nenhuma captura encontrada para este registro")
    return catches

@router.get("/espécie/{species_id}", response_model=List[CatchSchema])
def get_catches_by_species(
    species_id: int,
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Obter capturas de uma espécie específica"""
    catches = CatchesService.get_catches_by_species(db, species_id, limit=limit)
    if not catches:
        raise HTTPException(status_code=404, detail="Nenhuma captura encontrada para esta espécie")
    return catches

@router.get("/{catch_id}", response_model=CatchSchema)
def get_catch(
    catch_id: int,
    db: Session = Depends(get_db)
):
    """Obter detalhes de uma captura"""
    db_catch = CatchesService.get_catch_by_id(db, catch_id)
    if not db_catch:
        raise HTTPException(status_code=404, detail="Captura não encontrada")
    return db_catch

@router.get("/média/espécie/{species_id}")
def get_average_weight_by_species(
    species_id: int,
    db: Session = Depends(get_db)
):
    """Obter peso médio de uma espécie"""
    avg_weight = CatchesService.get_average_weight_by_species(db, species_id)
    return {"species_id": species_id, "average_weight_kg": avg_weight}

@router.post("/", response_model=CatchSchema, status_code=201)
def create_catch(
    catch_data: CatchCreateSchema,
    db: Session = Depends(get_db)
):
    """Registrar nova captura"""
    return CatchesService.create_catch(db, catch_data)

@router.put("/{catch_id}", response_model=CatchSchema)
def update_catch(
    catch_id: int,
    catch_data: CatchCreateSchema,
    db: Session = Depends(get_db)
):
    """Atualizar informações de uma captura"""
    db_catch = CatchesService.update_catch(db, catch_id, catch_data.dict(exclude_unset=True))
    if not db_catch:
        raise HTTPException(status_code=404, detail="Captura não encontrada")
    return db_catch

@router.delete("/{catch_id}", status_code=204)
def delete_catch(
    catch_id: int,
    db: Session = Depends(get_db)
):
    """Deletar uma captura"""
    if not CatchesService.delete_catch(db, catch_id):
        raise HTTPException(status_code=404, detail="Captura não encontrada")
    return None
