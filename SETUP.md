# NOA - Evolution API Local Setup

## 🚀 Despliegue Local Completo

Este setup despliega:
- ✅ **Evolution API Local**: Control total sin depender de servicio externo
- ✅ **NOA Bot**: Bot completo con análisis AI y RAG
- ✅ **PostgreSQL + Redis**: Para Evolution API
- ✅ **SQLite**: Para datos de NOA (fácil desarrollo)

## 📋 Requisitos Previos

1. **Docker + Docker Compose**
2. **Tu IP Pública**: Para que Evolution API pueda recibir webhooks
3. **OpenAI API Key**: Para análisis de IA

## 🛠️ Configuración

### 1. Configurar tu IP pública
```bash
# Obtener tu IP pública
curl ifconfig.me
# Ejemplo: 190.123.45.67
```

Edita `app/services/evolution.py` y reemplaza `tu-ip-pública` con tu IP real.

### 2. Configurar OpenAI API Key
```bash
export OPENAI_API_KEY=sk-proj-tu-key-aqui
```

## 🚀 Despliegue

```bash
# Construir y levantar todos los servicios
docker-compose up -d --build

# Ver logs
docker-compose logs -f noa-bot
docker-compose logs -f evolution-api
```

## 🌐 Servicios Desplegados

| Servicio | URL Local | Descripción |
|---------|------------|-------------|
| Evolution API | http://localhost:8080 | API local de WhatsApp |
| Evolution Manager | http://localhost:8080/manager | Panel de administración |
| NOA Bot | http://localhost:2311 | Bot conversacional |
| NOA Health | http://localhost:2311/health | Estado del bot |

## 📱 Configurar WhatsApp

### Paso 1: Crear Instancia
```bash
# Reemplazar TU_API_KEY_DE_EVOLUTION con tu key de Evolution API
curl -X POST http://localhost:8080/instance/create \
  -H "Content-Type: application/json" \
  -H "apikey: TU_API_KEY_DE_EVOLUTION" \
  -d '{
    "instanceName": "NOA_PROD",
    "integration": "WHATSAPP-BAILEYS",
    "number": "528442278408",
    "qrcode": true
  }'
```

### Paso 2: Configurar Webhook de NOA Bot
```bash
# Configurar webhook para que Evolution API envíe mensajes a NOA Bot
curl -X POST http://localhost:8080/webhook/set/NOA_PROD \
  -H "Content-Type: application/json" \
  -H "apikey: TU_API_KEY_DE_EVOLUTION" \
  -d '{
    "url": "http://localhost:2311/api/v1/webhook",
    "webhook_by_events": true,
    "base64": false
  }'
```

**Nota:** Los webhooks de n8n se configuran en el archivo .env de NOA Bot (ver .env.example), no en Evolution API.

## 🧪 Testing Local

```bash
# Test health check
curl http://localhost:2311/health

# Test webhook (simula mensaje de WhatsApp)
curl -X POST http://localhost:2311/api/v1/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "event": "messages.upsert",
    "data": {
      "key": {
        "remoteJid": "5218441026472@s.whatsapp.net",
        "fromMe": false,
        "id": "test_001"
      },
      "message": {
        "conversation": "Hola quiero información"
      }
    }
  }'
```

## 📊 Flujo Completo

1. **Hola** → Bienvenida 👋
2. **Nombre** → "Marco" → Pregunta industria 😊
3. **Industria** → "Tecnología" → Pregunta redes 📱
4. **Redes** → "@marco_tech" → Pregunta problema 📝
5. **Problema** → "Necesito más clientes" → 📊 **Análisis AI + RAG**
6. **Recomendación** → Basado en scoring → 🎯 Plan sugerido

## 🔧 Gestión

```bash
# Ver logs en tiempo real
docker-compose logs -f

# Detener todos los servicios
docker-compose down

# Reconstruir solo NOA
docker-compose up -d --build --no-deps noa-bot

# Limpiar datos
docker-compose down -v
```

## 🌟 Ventajas del Setup Local

- ✅ **Control Total**: Sin depender de APIs externas
- ✅ **Rápido Desarrollo**: Todo en tu máquina
- ✅ **Datos Locales**: Información de leads en tu DB
- ✅ **Costos Cero**: Sin costos de servicios de terceros
- ✅ **Full Debug**: Acceso a todos los logs y estados

## 🎯 Arquitectura

```
┌─────────────────────────────────────────┐
│ Internet                             │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│ Evolution API (Docker)              │
│ - http://localhost:8080            │
│ - PostgreSQL + Redis                 │
│ - Webhook → NOA Bot                │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│ NOA Bot (Docker)                   │
│ - http://localhost:2311            │
│ - FastAPI + SQLAlchemy            │
│ - OpenAI + RAG                    │
│ - SQLite DB                        │
│ - Webhooks duales                   │
└─────────────────────────────────────┘
```

**🚀 ¡Listo para desarrollo y producción local!**