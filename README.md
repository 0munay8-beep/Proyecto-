# Sistema Inteligente de Gestión de Transporte Público 🚌

> Sistema avanzado de monitoreo, optimización y gestión de flotas con **Álgebra Lineal**, **Machine Learning**, y **Visualización Interactiva**.

## 🎯 Características

### ✅ Base Implementada
- API REST con FastAPI
- Base de datos PostgreSQL
- Redis para caching
- Docker + Docker Compose

### 🚀 Mejoras Avanzadas (+85 puntos)

#### 🤖 Machine Learning Avanzado (+15)
- ✅ Clustering de patrones (K-means con normalización)
- ✅ Forecasting de demanda (Prophet con ARIMA)
- ✅ Detección de anomalías (Isolation Forest + Z-score)
- ✅ Clasificación de incidentes (Random Forest + Gradient Boosting)

#### 📐 Álgebra Lineal Avanzada (+18)
- ✅ Transformaciones de coordenadas GPS (matriz de rotación)
- ✅ Cálculo de distancias (Haversine + Manhattan)
- ✅ Eigenvalores para análisis de congestión
- ✅ Descomposición SVD para compresión de datos
- ✅ Interpolación polinómica de rutas
- ✅ Regresión lineal para predicción de tiempos

#### 🗺️ Visualización Interactiva de Mapas (+15)
- ✅ Polylines precisas de rutas con interpolación
- ✅ Hover info panels con datos en tiempo real
- ✅ Heat maps de congestión (gradiente de colores)
- ✅ Clusters dinámicos de buses
- ✅ Animación suave de movimiento
- ✅ Gestión optimizada de layers

#### 🗺️ Optimización de Rutas Tiempo Real (+20)
- ✅ Algoritmo genético para rebalanceo
- ✅ Simulated annealing para ajustes
- ✅ Programación dinámica para rutas óptimas

#### 🔔 Notificaciones Inteligentes (+10)
- ✅ Push, Email, SMS y Telegram
- ✅ Prioritización automática

#### 📊 Análisis Histórico (+8)
- ✅ Dashboard 6 meses
- ✅ Tendencias estacionales

#### 🎫 Tickets Inteligente (+10)
- ✅ Auto-generación y priorización

#### 🔐 Seguridad (+10)
- ✅ JWT + RBAC + Audit Logs

#### 🧪 Testing (+8)
- ✅ Unit + Integration + Load tests

## 📁 Estructura del Proyecto

```
Proyecto-/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── user.py
│   │   │   ├── bus.py
│   │   │   ├── route.py
│   │   │   ├── incident.py
│   │   │   ├── maintenance_ticket.py
│   │   │   └── analytics.py
│   │   ├── schemas/
│   │   ├── api/
│   │   ├── services/
│   │   ├── ml/
│   │   ├── utils/
│   │   ├── security/
│   │   └── tasks/
│   ├── tests/
│   ├── migrations/
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Map/
│   │   │   ├── Dashboard/
│   │   │   └── Widgets/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── utils/
│   │   └── App.jsx
│   └── package.json
├── scripts/
│   ├── setup.sh
│   ├── setup.bat
│   └── deploy.sh
├── docs/
│   ├── ARCHITECTURE.md
│   ├── API.md
│   ├── SETUP.md
│   ├── MATH.md
│   └── MAPPING.md
├── docker-compose.yml
├── .gitignore
└── README.md
```

## 🚀 Quick Start

### Con Script Automatizado (Recomendado)

```bash
# Linux/Mac
bash scripts/setup.sh

# Windows
scripts\setup.bat
```

### Manual

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
docker-compose up -d
```

## 📚 Documentación

- [Arquitectura](docs/ARCHITECTURE.md) - Diseño del sistema
- [API](docs/API.md) - Endpoints
- [Álgebra Lineal](docs/MATH.md) - Cálculos matemáticos
- [Mapas](docs/MAPPING.md) - Visualización
- [Setup](docs/SETUP.md) - Instalación

## 🧮 Tecnologías

**Backend**: FastAPI, SQLAlchemy, PostgreSQL, Redis
**ML**: Scikit-learn, Prophet, NumPy, SciPy
**Algebra**: NumPy, SciPy (SVD, Eigenvalues)
**Maps**: Leaflet, Folium
**DevOps**: Docker, Compose
**Testing**: Pytest, Locust

## 📊 Puntuación Total: 114 puntos 🎯

---

**Autor**: manuelat3104-prog
**Versión**: 1.0.0
**Última actualización**: 2026-05-30