import json
import os
from sqlalchemy.orm import Session
from backend.database import SessionLocal, engine
from backend.models import FishingSpot, Species
from backend.models.base import Base

def seed_database():
    """Carregar dados iniciais no banco de dados"""
    
    # Criar tabelas
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Limpar dados existentes (opcional)
        # db.query(FishingSpot).delete()
        # db.query(Species).delete()
        # db.commit()
        
        # Carregar espécies
        with open('data/species_catalog.json', 'r', encoding='utf-8') as f:
            species_data = json.load(f)
            
            for species_info in species_data['species']:
                existing = db.query(Species).filter(
                    Species.common_name == species_info['common_name']
                ).first()
                
                if not existing:
                    species = Species(
                        common_name=species_info['common_name'],
                        scientific_name=species_info.get('scientific_name'),
                        family=species_info.get('family'),
                        description=species_info.get('description'),
                        average_weight_kg=species_info.get('average_weight_kg'),
                        max_weight_kg=species_info.get('max_weight_kg'),
                        average_length_cm=species_info.get('average_length_cm'),
                        max_length_cm=species_info.get('max_length_cm'),
                        habitat=species_info.get('habitat'),
                        best_season=species_info.get('best_season'),
                        best_tide_phase=species_info.get('best_tide_phase'),
                        best_hours=species_info.get('best_hours'),
                        depth_range=species_info.get('depth_range'),
                    )
                    db.add(species)
                    print(f"✓ Espécie adicionada: {species.common_name}")
        
        # Carregar pontos de pesca
        with open('data/fishing_spots_recife.json', 'r', encoding='utf-8') as f:
            spots_data = json.load(f)
            
            for spot_info in spots_data['fishing_spots']:
                existing = db.query(FishingSpot).filter(
                    FishingSpot.name == spot_info['name']
                ).first()
                
                if not existing:
                    spot = FishingSpot(
                        name=spot_info['name'],
                        latitude=spot_info['latitude'],
                        longitude=spot_info['longitude'],
                        description=spot_info.get('description'),
                        access_type=spot_info.get('access_type'),
                        depth_avg=spot_info.get('depth_avg'),
                        bottom_type=spot_info.get('bottom_type'),
                        average_rating=spot_info.get('average_rating', 0.0),
                        visits_count=spot_info.get('visits_count', 0),
                        success_rate=spot_info.get('success_rate', 0.0),
                        notes=spot_info.get('notes'),
                    )
                    db.add(spot)
                    print(f"✓ Ponto adicionado: {spot.name}")
        
        db.commit()
        print("\n✅ Dados iniciais carregados com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao carregar dados: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🎣 Carregando dados iniciais do PescaRec-Sistema...\n")
    seed_database()
    print("\n✅ Script concluído!")
