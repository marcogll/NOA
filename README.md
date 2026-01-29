# NOA - Networked Operational Assistant

NOA es un asistente conversacional inteligente para WhatsApp, diseñado para Noire Collective. Su objetivo es automatizar la calificación de leads, analizar el sentimiento de los prospectos y recomendar servicios específicos mediante un motor RAG (Retrieval-Augmented Generation).

## 🚀 Funcionalidades Actuales

### 💬 Conversaciones Inteligentes
- **Flujo Estructurado**: FSM con 8 estados (INIT → ASK_NAME → ASK_INDUSTRY → ASK_SOCIAL_MEDIA → ASK_PROBLEM → ANALYZE → RECOMMEND → CLOSED)
- **Respuestas en Español**: Todas las interacciones en español con emojis estratégicos
- **Gestión de Sesiones**: Seguimiento del estado de cada conversación

### 🧠 Análisis con IA
- **OpenAI Integration**: Análisis de sentimiento, intención y scoring de leads (0-100)
- **Motor RAG**: Recomendaciones personalizadas basadas en catálogo real de servicios y planes
- **Data Real**: Usa archivos `data/services.json` y `data/plan.json` para recomendaciones

### 📊 Gestión de Leads
- **Scoring Automático**: Calificación de prospectos basada en análisis de conversación
- **Registro Completo**: Captura de nombre, industria, redes sociales, problemas y análisis
- **Webhooks Duales**: Envío de datos a producción y test con UUID único

### 🔧 Integraciones
- **Evolution API**: WhatsApp en producción (instancia: AD4F74469C6C-450A-AF74-20B17F8E4942)
- **Database Asincrónica**: PostgreSQL con asyncpg para alto rendimiento
- **Sistema de Migraciones**: Alembic configurado para producción

## 🛠️ Stack Tecnológico

- **Lenguaje**: Python 3.11+
- **Framework Web**: FastAPI (Puerto 2311)
- **LLM**: OpenAI API (GPT-4 & GPT-3.5-turbo)
- **Mensajería**: Evolution API (WhatsApp)
- **Base de Datos**: PostgreSQL con async operations
- **Cache**: Redis (sesiones futuras)
- **Migraciones**: Alembic
- **Testing**: Pytest con async support

## 📁 Estructura Actual

```text
NOA/
├── app/
│   ├── main.py              # Entry point (puerto 2311)
│   ├── config.py            # Configuración y .env
│   ├── routes/              # API endpoints
│   │   └── webhooks.py     # Webhook de Evolution API
│   ├── services/            # Integraciones
│   │   ├── openai.py       # Análisis de IA
│   │   ├── rag.py          # Motor RAG
│   │   ├── webhook.py      # Webhooks duales (prod/test)
│   │   ├── sentiment.py    # Análisis de sentimiento
│   │   └── evolution.py    # WhatsApp API
│   ├── schemas/             # Validación de datos
│   │   └── webhooks.py     # Schemas para payloads
│   ├── db/                  # Base de datos
│   │   ├── models.py       # Modelo Lead
│   │   ├── session.py      # Sesión síncrona
│   │   └── async_session.py # Sesión asíncrona
│   ├── flows/               # FSM
│   │   └── states.py       # Estados conversacionales
│   └── alembic/             # Migraciones
├── data/                    # Catálogos reales
│   ├── services.json       # Servicios individuales
│   └── plan.json           # Planes mensuales
├── tests/                   # Tests
└── .env                     # Configuración de producción
```

## 📖 Flujo Conversacional

1. **INIT**: Bienvenida y solicitud de nombre 👋
2. **ASK_NAME**: Captura de nombre
3. **ASK_INDUSTRY**: Identificación de industria 📱
4. **ASK_SOCIAL_MEDIA**: Recolección de redes sociales
5. **ASK_PROBLEM**: Captura del problema principal 📝
6. **ANALYZE**: Análisis con OpenAI (sentimiento, intención, score)
7. **RECOMMEND**: Recomendación personalizada 🎯
8. **CLOSED**: Cierre y envío de datos

## ⚙️ Configuración de Producción

### Variables de Entorno
```bash
# OpenAI
OPENAI_API_KEY=sk-...

# Evolution API
EVOLUTION_API_URL=https://evolution.soul23.cloud/
EVOLUTION_API_TOKEN=
EVOLUTION_INSTANCE=AD4F744....

# Webhooks duales
EXTERNAL_WEBHOOK_URL_PROD=
EXTERNAL_WEBHOOK_URL_TEST=

# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_SERVER=db
POSTGRES_DB=noa_db
```

### Ejecución
```bash
# Desarrollo
python -m app.main

# Producción (puerto 2311)
uvicorn app.main:app --host 0.0.0.0 --port 2311

# Tests
pytest tests/ -v
```

## 📊 Webhook Payload

Cada lead completo se envía con esta estructura:
```json
{
  "uuid": "uuid-único",
  "timestamp": "2024-01-29T18:30:00Z",
  "source": "NOA_BOT",
  "instance": "AD4F74469C6C-450A-AF74-20B17F8E4942",
  "data": {
    "phone": "+1234567890",
    "name": "Juan Pérez",
    "industry": "Restaurantes",
    "social_media": "@restaurant_ejemplo",
    "problem": "Necesito más clientes",
    "sentiment": "positive",
    "intent": "marketing_consultation",
    "lead_score": 85,
    "recommended_service": "Plan Gold",
    "state": "CLOSED"
  }
}
```

## 🔍 Estado Actual del Proyecto

### ✅ Completado
- Flujo conversacional completo
- Análisis con OpenAI integrado
- Sistema RAG con data real
- Webhooks duales funcionando
- Base de datos asíncrona
- Validación de inputs
- Error handling
- Migraciones configuradas
- Tests básicos

### 🔄 Próximo Sprint
- Integración Redis para sesiones
- Sistema de rate limiting
- Monitoring y métricas
- Tests de integración completos
- Documentación API

---

**NOA v1.0** - Asistente conversacional para Noire Collective  
*Desarrollado con ❤️ para automatización de leads*