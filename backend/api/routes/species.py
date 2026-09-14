from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.services.species_service import SpeciesService
from backend.schemas.species import SpeciesSchema, SpeciesCreateSchema

router = APIRouter(
    prefix="/espécies",
    tags=["Espécies de Peixe"],
    responses={404: {"description": "Espécie não encontrada"}},
)

@router.get("/", response_model=List[SpeciesSchema])
def list_species(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Listar todas as espécies de peixes"""
    return SpeciesService.get_all_species(db, skip=skip, limit=limit)

@router.get("/buscar", response_model=List[SpeciesSchema])
def search_species(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    """Buscar espécies por nome"""
    species = SpeciesService.search_species(db, q)
    if not species:
        raise HTTPException(status_code=404, detail="Nenhuma espécie encontrada")
    return species

@router.get("/{species_id}", response_model=SpeciesSchema)
def get_species(
    species_id: int,
    db: Session = Depends(get_db)
):
    """Obter detalhes de uma espécie"""
    db_species = SpeciesService.get_species_by_id(db, species_id)
    if not db_species:
        raise HTTPException(status_code=404, detail="Espécie não encontrada")
    return db_species

@router.get("/sazonalidade/{season}", response_model=List[SpeciesSchema])
def get_species_by_season(
    season: str,
    db: Session = Depends(get_db)
):
    """Obter espécies por estação do ano"""
    species = SpeciesService.get_species_by_season(db, season)
    if not species:
        raise HTTPException(status_code=404, detail="Nenhuma espécie encontrada para esta estação")
    return species

@router.post("/", response_model=SpeciesSchema, status_code=201)
def create_species(
    species_data: SpeciesCreateSchema,
    db: Session = Depends(get_db)
):
    """Criar nova espécie de peixe"""
    return SpeciesService.create_species(db, species_data)

@router.put("/{species_id}", response_model=SpeciesSchema)
def update_species(
    species_id: int,
    species_data: SpeciesCreateSchema,
    db: Session = Depends(get_db)
):
    """Atualizar informações de uma espécie"""
    db_species = SpeciesService.update_species(db, species_id, species_data.dict(exclude_unset=True))
    if not db_species:
        raise HTTPException(status_code=404, detail="Espécie não encontrada")
    return db_species

@router.delete("/{species_id}", status_code=204)
def delete_species(
    species_id: int,
    db: Session = Depends(get_db)
):
    """Deletar uma espécie"""
    if not SpeciesService.delete_species(db, species_id):
        raise HTTPException(status_code=404, detail="Espécie não encontrada")
    return None
