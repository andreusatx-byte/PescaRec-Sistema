# 🎣 PescaRec-Sistema
**Sistema Inteligente de Análise de Marés, Localização de Pontos de Pesca e Registro de Sucesso de Pescarias**

## 📍 Região: Metropolitana do Recife - PE

---

## 🎯 Objetivo
Desenvolver uma plataforma integrada que combine dados de tábuas de marés, localização geográfica de pontos de pesca, marcação de locais já visitados e análise de sucesso de pescarias para otimizar as saídas de pesca na região metropolitana do Recife.

## 📋 Funcionalidades Principais

### 1. **Análise de Tábuas de Marés**
- Integração com dados de marés em tempo real
- Previsão de marés para os próximos dias
- Identificação dos melhores horários para pesca
- Histórico de comportamento das marés

### 2. **Mapa de Pontos de Pesca**
- Localização geográfica dos melhores pontos de pesca
- Classificação por tipo de peixe
- Profundidade e características do fundo
- Acesso por terra, barco ou estrutura existente

### 3. **Registro de Locais Visitados**
- Marcação de pontos já explorados
- Histórico de visitas por data
- Avaliação de sucesso (peixes capturados)
- Notas e observações do pescador

### 4. **Banco de Dados de Peixes**
- Espécies encontradas em cada ponto
- Sazonalidade das espécies
- Tamanho e peso médio capturado
- Melhor época para cada espécie

### 5. **Análise de Sucesso**
- Taxa de captura por ponto
- Melhor horário e condição de maré
- Recomendações baseadas em histórico
- Estatísticas e gráficos comparativos

### 6. **Sugestões Inteligentes**
- Recomendação de pontos com base na maré atual
- Sugestão de espécies sazonais
- Alertas de condições ideais
- Previsão de demanda de pontos populares

---

## 🏗️ Estrutura do Projeto

```
PescaRec-Sistema/
├── backend/
│   ├── api/
│   ├── models/
│   ├── services/
│   └── database/
├── frontend/
│   ├── pages/
│   ├── components/
│   └── maps/
├── data/
│   ├── tides/
│   ├── fishing-spots/
│   └── species/
├── docs/
└── requirements.txt
```

---

## 🌊 Dados de Marés - Recife PE

### Referências Locais
- **Porto de Recife** - Coordenadas: -8.0833, -34.8711
- **Barra de Catuama** - Coordenadas: -7.9897, -34.8206
- **Barra de Santo Antônio** - Coordenadas: -7.9000, -34.8500
- **Jaboatão dos Guararapes** - Coordenadas: -8.1167, -34.9667
- **Olinda** - Coordenadas: -8.0089, -34.8553

### APIs de Marés Sugeridas
- NOAA Tides & Currents
- Tidal API
- OpenWeatherMap (integração com condições)

---

## 📊 Pontos de Pesca Iniciais (Recife Metropolitana)

| Local | Coordenadas | Tipo de Pesca | Espécies Comuns | Acesso |
|-------|------------|--------------|-----------------|--------|
| Barra de Catuama | -7.9897, -34.8206 | Barco/Praia | Pargo, Garoupa | Barco |
| Recife de Coral | -8.0833, -34.8711 | Mergulho/Snorkel | Peixe Dourado, Garoupa | Barco |
| Praia de Boa Viagem | -8.1194, -34.8806 | Praia/Arremesso | Tainha, Xaréu | A Pé |
| Jaboatão dos Guararapes | -8.1167, -34.9667 | Barco | Pargo, Badejo | Barco |
| Porto de Recife | -8.0833, -34.8711 | Cais | Sardinha, Cavala | A Pé |

---

## 🛠️ Tecnologias Propostas

### Backend
- **Python** (Flask/FastAPI)
- **PostgreSQL** (Banco de dados principal)
- **Redis** (Cache de dados de marés)
- **Celery** (Agendamento de tarefas)

### Frontend
- **React/Vue.js** (Interface web)
- **Leaflet/Google Maps** (Integração de mapas)
- **Chart.js/D3.js** (Visualização de dados)

### Integrações
- API NOAA Tides & Currents
- Google Maps API
- OpenWeatherMap API
- Banco de dados colaborativo local

---

## 📝 Como Contribuir

1. Clone o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/sua-feature`)
3. Commit suas mudanças (`git commit -m 'Add sua-feature'`)
4. Push para a branch (`git push origin feature/sua-feature`)
5. Abra um Pull Request

---

## 📞 Contato & Suporte

Para dúvidas, sugestões ou reporte de bugs, abra uma **Issue** neste repositório.

---

## 📄 Licença
Este projeto está sob licença MIT.

---

**Última atualização:** Setembro de 2026
