# 🏗️ Arquitetura do Sistema PescaRec

## 1. Visão Geral da Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React/Vue)                     │
│         Dashboard | Mapas | Gráficos | Formulários             │
└──────────────────────┬──────────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────────┐
│                    REST API (FastAPI/Flask)                     │
│  ├─ /marés          ├─ /pontos          ├─ /registros         │
│  ├─ /espécies       ├─ /recomendações   └─ /análises          │
└──────────────────────┬──────────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
┌───────▼──────┐  ┌────▼────┐  ┌────▼────────┐
│  PostgreSQL  │  │  Redis  │  │  APIs Ext.  │
│   (BD Prin)  │  │  (Cache)│  │ (NOAA, OWM) │
└──────────────┘  └─────────┘  └─────────────┘
```

## 2. Componentes Principais

### 2.1 Módulo de Marés
**Responsabilidade:** Gerenciar dados de tábuas de marés

```python
# services/tides_service.py
class TidesService:
    - get_current_tide(location, date)
    - get_tide_forecast(location, days=7)
    - get_best_fishing_hours(location, date)
    - calculate_tide_cycle()
```

**Endpoints:**
- `GET /api/marés/atual?local=recife`
- `GET /api/marés/previsão?local=recife&dias=7`
- `GET /api/marés/horários-ideais?local=recife&data=2026-09-15`

### 2.2 Módulo de Pontos de Pesca
**Responsabilidade:** Gerenciar localização e características de pontos

```python
# services/fishing_spots_service.py
class FishingSpotsService:
    - create_spot(name, coords, description)
    - get_all_spots()
    - get_spot_by_id(spot_id)
    - update_spot_rating(spot_id, rating)
    - get_spots_by_radius(center_coords, radius_km)
```

**Endpoints:**
- `GET /api/pontos` → Lista todos os pontos
- `GET /api/pontos/{id}` → Detalhes do ponto
- `POST /api/pontos` → Criar novo ponto
- `GET /api/pontos/raio?lat=-8.0833&lon=-34.8711&raio=10`

### 2.3 Módulo de Registros de Pesca
**Responsabilidade:** Gerenciar histórico de visitas e capturas

```python
# services/fishing_records_service.py
class FishingRecordsService:
    - create_record(spot_id, date, tide_info, catches)
    - get_records_by_spot(spot_id)
    - get_records_by_fisher(fisher_id)
    - calculate_success_rate(spot_id)
    - export_records(format='csv'|'json')
```

**Endpoints:**
- `POST /api/registros` → Registrar nova pescaria
- `GET /api/registros?ponto_id=1` → Histórico de um ponto
- `GET /api/registros/taxa-sucesso?ponto_id=1` → Taxa de captura

### 2.4 Módulo de Espécies
**Responsabilidade:** Gerenciar catálogo de peixes e sazonalidade

```python
# services/species_service.py
class SpeciesService:
    - get_all_species()
    - get_species_by_location(location)
    - get_species_seasonality(species_name)
    - add_catch_record(species_id, weight, length, spot_id)
```

**Endpoints:**
- `GET /api/espécies` → Lista todas as espécies
- `GET /api/espécies?local=recife` → Espécies por local
- `GET /api/espécies/sazonalidade?espécie=pargo` → Melhor época

### 2.5 Módulo de Recomendações
**Responsabilidade:** Fornecer sugestões inteligentes

```python
# services/recommendations_service.py
class RecommendationsService:
    - recommend_spots(current_tide, date, fisher_preferences)
    - recommend_species(current_season, location)
    - recommend_fishing_time(location, date)
    - get_alerts(location)
```

**Endpoints:**
- `GET /api/recomendações/pontos?data=2026-09-15` → Pontos recomendados
- `GET /api/recomendações/espécies?estação=primavera` → Espécies sazonais
- `GET /api/recomendações/horários?local=recife&data=2026-09-15` → Melhor hora
- `GET /api/alertas?local=recife` → Alertas ativos

## 3. Modelo de Dados

### 3.1 Tabelas Principais

```sql
-- Pontos de Pesca
CREATE TABLE fishing_spots (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    description TEXT,
    access_type VARCHAR(50), -- 'barco', 'praia', 'cais'
    depth_avg INT,
    bottom_type VARCHAR(100),
    average_rating FLOAT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Registros de Pesca
CREATE TABLE fishing_records (
    id SERIAL PRIMARY KEY,
    spot_id INT REFERENCES fishing_spots(id),
    fisher_id INT,
    fishing_date DATE,
    tide_level VARCHAR(50), -- 'alta', 'média', 'baixa'
    tide_phase VARCHAR(50), -- 'enchente', 'vazante'
    weather_condition VARCHAR(100),
    total_catches INT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Capturas de Peixes
CREATE TABLE catches (
    id SERIAL PRIMARY KEY,
    record_id INT REFERENCES fishing_records(id),
    species_id INT REFERENCES species(id),
    weight_kg FLOAT,
    length_cm INT,
    captured_at TIME,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Espécies de Peixe
CREATE TABLE species (
    id SERIAL PRIMARY KEY,
    common_name VARCHAR(255), -- 'Pargo', 'Garoupa', etc.
    scientific_name VARCHAR(255),
    description TEXT,
    average_weight_kg FLOAT,
    average_length_cm INT,
    habitat VARCHAR(100),
    best_season VARCHAR(50),
    best_tide_phase VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Relação Espécies x Locais
CREATE TABLE species_locations (
    id SERIAL PRIMARY KEY,
    species_id INT REFERENCES species(id),
    spot_id INT REFERENCES fishing_spots(id),
    frequency VARCHAR(50), -- 'rara', 'ocasional', 'comum', 'muito_comum'
    last_recorded DATE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## 4. Fluxo de Dados

### 4.1 Caso de Uso: Registrar Novo Ponto de Pesca
```
Fisher
  ↓
[Formulário Web]
  ↓
POST /api/pontos
  ↓
[Validação]
  ↓
[BD PostgreSQL]
  ↓
[Cache Redis]
  ↓
[Resposta JSON]
  ↓
[Atualização Mapa]
```

### 4.2 Caso de Uso: Obter Recomendações
```
Fisher consulta app
  ↓
GET /api/recomendações/pontos
  ↓
[API NOAA - Dados Marés]
  ↓
[BD PostgreSQL - Histórico]
  ↓
[Cache Redis - Taxa Sucesso]
  ↓
[Algoritmo Recomendação]
  ↓
[Ranking Pontos]
  ↓
[Resposta JSON com GeoJSON]
  ↓
[Visualização Mapa]
```

## 5. Segurança

- **Autenticação:** JWT Tokens
- **Autorização:** Role-based Access Control (RBAC)
- **Validação:** Schemas com Pydantic (FastAPI) ou Marshmallow (Flask)
- **Rate Limiting:** Implementado via Redis
- **HTTPS:** Obrigatório em produção

## 6. Escalabilidade

- **Caching:** Redis para dados frequentemente acessados
- **Async:** Celery para tarefas pesadas (processamento de marés)
- **Database:** Índices em lat/lon para queries geoespaciais
- **API Gateway:** Nginx para load balancing

---

**Versão:** 1.0
**Data:** Setembro de 2026
