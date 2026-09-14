from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.services.fishing_spots_service import FishingSpotsService
from backend.schemas.fishing_spot import FishingSpotSchema, FishingSpotCreateSchema

router = APIRouter(
    prefix="/pontos",
    tags=["Pontos de Pesca"],
    responses={404: {"description": "Ponto não encontrado"}},
)

@router.get("/", response_model=List[FishingSpotSchema])
def list_spots(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Listar todos os pontos de pesca"""
    return FishingSpotsService.get_all_spots(db, skip=skip, limit=limit)

@router.get("/melhores-avaliados", response_model=List[FishingSpotSchema])
def get_best_rated_spots(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Obter pontos melhor avaliados"""
    return FishingSpotsService.get_best_rated_spots(db, limit=limit)

@router.get("/mais-visitados", response_model=List[FishingSpotSchema])
def get_most_visited_spots(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Obter pontos mais visitados"""
    return FishingSpotsService.get_most_visited_spots(db, limit=limit)

@router.get("/raio", response_model=List[FishingSpotSchema])
def get_spots_by_radius(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    raio: float = Query(10.0, ge=0.1),
    db: Session = Depends(get_db)
):
    """Obter pontos dentro de um raio (em km)"""
    spots = FishingSpotsService.get_spots_by_radius(db, latitude, longitude, raio)
    if not spots:
        raise HTTPException(status_code=404, detail="Nenhum ponto encontrado nesta área")
    return spots

@router.get("/buscar", response_model=List[FishingSpotSchema])
def search_spots(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    """Buscar pontos por nome"""
    spots = FishingSpotsService.get_spots_by_name(db, q)
    if not spots:
        raise HTTPException(status_code=404, detail="Nenhum ponto encontrado")
    return spots

@router.get("/{spot_id}", response_model=FishingSpotSchema)
def get_spot(
    spot_id: int,
    db: Session = Depends(get_db)
):
    """Obter detalhes de um ponto de pesca"""
    db_spot = FishingSpotsService.get_spot_by_id(db, spot_id)
    if not db_spot:
        raise HTTPException(status_code=404, detail="Ponto não encontrado")
    return db_spot

@router.post("/", response_model=FishingSpotSchema, status_code=201)
def create_spot(
    spot_data: FishingSpotCreateSchema,
    db: Session = Depends(get_db)
):
    """Criar novo ponto de pesca"""
    return FishingSpotsService.create_spot(db, spot_data)

@router.put("/{spot_id}", response_model=FishingSpotSchema)
def update_spot(
    spot_id: int,
    spot_data: FishingSpotCreateSchema,
    db: Session = Depends(get_db)
):
    """Atualizar informações de um ponto de pesca"""
    db_spot = FishingSpotsService.update_spot(db, spot_id, spot_data.dict(exclude_unset=True))
    if not db_spot:
        raise HTTPException(status_code=404, detail="Ponto não encontrado")
    return db_spot

@router.delete("/{spot_id}", status_code=204)
def delete_spot(
    spot_id: int,
    db: Session = Depends(get_db)
):
    """Deletar um ponto de pesca"""
    if not FishingSpotsService.delete_spot(db, spot_id):
        raise HTTPException(status_code=404, detail="Ponto não encontrado")
    return None
