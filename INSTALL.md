# 🎣 Guia de Instalação - PescaRec-Sistema

## Pré-requisitos

- Python 3.9+
- PostgreSQL 12+
- Redis 6.0+
- Git

## Passo 1: Clonar o Repositório

```bash
git clone https://github.com/andreusatx-byte/PescaRec-Sistema.git
cd PescaRec-Sistema
```

## Passo 2: Criar Virtual Environment

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

## Passo 3: Instalar Dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Passo 4: Configurar Variáveis de Ambiente

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas configurações locais:

```env
# Database
DATABASE_URL=postgresql://seu_usuario:sua_senha@localhost:5432/pescaRec_db

# Redis
REDIS_URL=redis://localhost:6379/0

# API Keys (obtenha em cada serviço)
NOAA_API_KEY=sua_chave_aqui
OPENWEATHERMAP_API_KEY=sua_chave_aqui
GOOGLE_MAPS_API_KEY=sua_chave_aqui

# JWT Secret
JWT_SECRET_KEY=gere_uma_chave_segura_aqui

# Debug
DEBUG=True
```

## Passo 5: Criar Banco de Dados

```bash
# PostgreSQL
createbdb -U postgres pescaRec_db
```

## Passo 6: Executar Migrações (Alembic)

```bash
# Criar inicial do banco
alembic upgrade head
```

## Passo 7: Carregar Dados Iniciais

```bash
python scripts/seed_data.py
```

Este script vai:
- Criar espécies de peixes
- Adicionar pontos de pesca do Recife
- Adicionar dados de exemplo

## Passo 8: Iniciar o Servidor

```bash
cd backend
python main.py
```

Ou:

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

A API estará disponível em: **http://localhost:8000**

## Acessar Documentação Interativa

- **Swagger UI:** http://localhost:8000/api/docs
- **ReDoc:** http://localhost:8000/api/redoc

## Estrutura de Pastas

```
PescaRec-Sistema/
├── backend/
│   ├── api/
│   │   ├── routes/          # Rotas da API
│   │   └── __init__.py
│   ├── models/          # Modelos de dados
│   ├── schemas/         # Schemas Pydantic
│   ├── services/        # Lógica de negócios
│   ├── database/        # Conexão e sessões
│   ├── config.py        # Configurações
│   └── main.py          # Aplicação principal
├─┐ frontend/         # Código do frontend (React/Vue)
├─┐ data/             # Dados iniciais (JSON)
├─┐ docs/             # Documentação
├─┐ scripts/          # Scripts de utilidade
├─┐ requirements.txt  # Dependências Python
└─┐ README.md         # Este arquivo
```

## Endpoints Principais

### Espécies
- `GET /api/espécies` - Listar todas as espécies
- `POST /api/espécies` - Criar nova espécie
- `GET /api/espécies/{id}` - Obter espécie por ID
- `GET /api/espécies/sazonalidade/{season}` - Espécies sazonais

### Pontos de Pesca
- `GET /api/pontos` - Listar todos os pontos
- `POST /api/pontos` - Criar novo ponto
- `GET /api/pontos/{id}` - Detalhes do ponto
- `GET /api/pontos/raio?lat=-8.0833&lon=-34.8711&raio=10` - Pontos em raio
- `GET /api/pontos/melhores-avaliados` - Melhores avaliados

### Registros de Pesca
- `GET /api/registros` - Listar registros
- `POST /api/registros` - Criar novo registro
- `GET /api/registros/ponto/{spot_id}` - Registros de um ponto
- `GET /api/registros/taxa-sucesso/{spot_id}` - Taxa de sucesso

### Capturas
- `GET /api/capturas/registro/{record_id}` - Capturas de um registro
- `POST /api/capturas` - Registrar captura
- `GET /api/capturas/espécie/{species_id}` - Capturas por espécie

## Resolvendo Problemas Comuns

### Erro: "PostgreSQL connection refused"

```bash
# Verifique se PostgreSQL está rodando
sudo service postgresql status

# Inicie o serviço
sudo service postgresql start
```

### Erro: "Redis connection refused"

```bash
# Verifique se Redis está rodando
redis-cli ping

# Inicie o serviço
redis-server
```

### Erro: "ModuleNotFoundError"

```bash
# Verifique se o venv está ativado
source venv/bin/activate

# Reinstale as dependências
pip install -r requirements.txt
```

## Desenvolvimento

### Executar Testes

```bash
pytest
```

### Verificar Código (Linting)

```bash
flake8 backend/
black backend/
mypy backend/
```

### Gerar Migração (Alembic)

```bash
alembic revision --autogenerate -m "descrição da mudança"
alembic upgrade head
```

## Contribuindo

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para diretrizes de contribuição.

## Suporte

Para dúvidas ou problemas, abra uma [Issue](https://github.com/andreusatx-byte/PescaRec-Sistema/issues).

---

**Última atualização:** Setembro de 2026
