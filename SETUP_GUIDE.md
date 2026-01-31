# NOA - Guía de Configuración y Despliegue

## 🎯 Objetivo
Guía completa para configurar y desplegar el proyecto NOA, sin exponer información sensible.

---

## 📋 Variables de Entorno Requeridas

Todas las variables sensibles se configuran en el archivo `.env`:

```bash
# OpenAI
OPENAI_API_KEY=sk-proj-TU_OPENAI_API_KEY_AQUI

# Evolution API
EVOLUTION_API_URL=http://evolution-api:8080  # Local
# EVOLUTION_API_URL=https://evolution.soul23.cloud/  # VPS
EVOLUTION_API_TOKEN=TU_API_KEY_DE_EVOLUTION_AQUI
EVOLUTION_INSTANCE=NOA_PROD

# Webhooks de n8n (obtenidos desde tu instancia de n8n)
EXTERNAL_WEBHOOK_URL_PROD=https://flows.soul23.cloud/webhook/TU_WEBHOOK_ID_PRODUCCION
EXTERNAL_WEBHOOK_URL_TEST=https://flows.soul23.cloud/webhook-test/TU_WEBHOOK_ID_TEST

# Database
DATABASE_URL=sqlite:///./noa_dev.db
# O para PostgreSQL en producción:
# DATABASE_URL=postgresql://user:password@host:5432/dbname
```

---

## 🚀 Configuración Local

### Paso 1: Crear Archivo .env

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar con tus valores
nano .env
# O usar tu editor preferido
```

### Paso 2: Verificar Configuración

```bash
# Verificar que las variables estén configuradas
cat .env | grep -v "^#"
```

### Paso 3: Levantar Contenedores

```bash
# Construir y levantar todos los servicios
docker-compose up -d --build

# Verificar estado de contenedores
docker-compose ps
```

**Esperado:**
```
NAME            STATUS
evolution-noa   Up X seconds        0.0.0.0:8080->8080/tcp
evolution-db     Up X seconds        5432/tcp
evolution-redis  Up X seconds        6379/tcp
noa-bot         Up X seconds        0.0.0.0.0:2311->8000/tcp
```

### Paso 4: Verificar Servicios

```bash
# Health check de Evolution API
curl http://localhost:8080

# Health check de NOA Bot
curl http://localhost:2311/health
```

---

## 📱 Configuración de WhatsApp (Evolution API v2.1.1)

### Paso 1: Crear Instancia

```bash
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

**Respuesta esperada:**
```json
{
  "instance": {
    "instanceName": "NOA_PROD",
    "instanceId": "<uuid>",
    "integration": "WHATSAPP-BAILEYS",
    "status": "connecting"
  },
  "hash": "<token>",
  "settings": { ... },
  "qrcode": {"count": 0}
}
```

### Paso 2: Obtener y Escanear QR Code

```bash
# Polling continuo hasta obtener QR code
while true; do
  response=$(curl -s -X GET http://localhost:8080/instance/connect/NOA_PROD \
      -H "apikey: TU_API_KEY_DE_EVOLUTION")

  # Verificar si hay QR code en base64
  if echo "$response" | grep -q "base64"; then
    echo "✅ QR Code generado exitosamente!"
    echo "$response" | python3 -m json.tool
    break
  fi

  # Verificar si ya está conectado
  if echo "$response" | grep -q '"state":"open"'; then
    echo "✅ Instancia ya está conectada!"
    break
  fi

  sleep 2
done
```

### Paso 3: Escanear QR Code

1. Abrir WhatsApp en el teléfono
2. Ir a **Ajustes** → **Dispositivos vinculados**
3. Tocar **Vincular dispositivo**
4. Escanear el QR code mostrado

**Importante:** El QR code expira en ~20 segundos, escanear rápidamente

### Paso 4: Verificar Conexión

```bash
curl -X GET http://localhost:8080/instance/connectionState/NOA_PROD \
  -H "apikey: TU_API_KEY_DE_EVOLUTION"
```

**Esperado:** `{"instance": {"instanceName": "NOA_PROD", "state": "open"}}`

### Paso 5: Configurar Webhook de NOA Bot

```bash
curl -X POST http://localhost:8080/webhook/set/NOA_PROD \
  -H "Content-Type: application/json" \
  -H "apikey: TU_API_KEY_DE_EVOLUTION" \
  -d '{
    "url": "http://localhost:2311/api/v1/webhook",
    "webhook_by_events": true,
    "base64": false
  }'
```

---

## 🌐 Configuración en VPS

### Paso 1: Conectar al VPS

```bash
# SSH al VPS (reemplazar con tus datos)
ssh user@ip-del-vps
```

### Paso 2: Clonar Repositorio

```bash
# Navegar al directorio de proyectos
cd ~/projects

# Clonar el repositorio (reemplazar URL)
git clone https://github.com/usuario/noa.git
cd noa

# Verificar contenido
ls -la
```

### Paso 3: Crear Archivo .env en VPS

```bash
# Crear .env con valores del VPS
cat > .env << 'EOF'
# OpenAI
OPENAI_API_KEY=sk-proj-TU_OPENAI_API_KEY_VPS

# Evolution API (VPS)
EVOLUTION_API_URL=http://evolution-api:8080
EVOLUTION_API_TOKEN=TU_API_KEY_DE_EVOLUTION_VPS
EVOLUTION_INSTANCE=NOA_PROD

# Webhooks de n8n
EXTERNAL_WEBHOOK_URL_PROD=https://flows.soul23.cloud/webhook/TU_WEBHOOK_ID_VPS
EXTERNAL_WEBHOOK_URL_TEST=https://flows.soul23.cloud/webhook-test/TU_WEBHOOK_ID_VPS

# Database
DATABASE_URL=sqlite:///./noa_dev.db
EOF

# Verificar creación
cat .env
```

### Paso 4: Levantar Contenedores en VPS

```bash
# Construir y levantar servicios
docker-compose up -d --build

# Verificar estado
docker-compose ps
```

### Paso 5: Configurar Instancia de WhatsApp en VPS

```bash
# Verificar si ya existe instancia
curl -X GET http://localhost:8080/instance/fetchInstances \
  -H "apikey: TU_API_KEY_DE_EVOLUTION_VPS"

# Si no existe, crearla
curl -X POST http://localhost:8080/instance/create \
  -H "Content-Type: application/json" \
  -H "apikey: TU_API_KEY_DE_EVOLUTION_VPS" \
  -d '{
    "instanceName": "NOA_PROD",
    "integration": "WHATSAPP-BAILEYS",
    "number": "528442278408",
    "qrcode": true
  }'
```

### Paso 6: Obtener y Escanear QR Code en VPS

```bash
# Polling del QR code en el VPS
while true; do
  response=$(curl -s -X GET http://localhost:8080/instance/connect/NOA_PROD \
      -H "apikey: TU_API_KEY_DE_EVOLUTION_VPS")

  if echo "$response" | grep -q "base64"; then
    echo "✅ QR Code generado!"
    echo "$response" | python3 -m json.tool
    break
  fi

  sleep 2
done
```

---

## 🔄 Flujo de Trabajo Git (Local → VPS)

### Workflow de Desarrollo

```
┌─────────────────────────────────┐
│ EQUIPO LOCAL (Desarrollo)    │
└─────────────┬───────────────┘
              │
              │ 1. Hacer cambios en código
              ▼
         [Editar archivos]
              │
              │ 2. Commit cambios
              ▼
         git add .
         git commit -m "feat: descripción"
              │
              │ 3. Push a GitHub/GitLab
              ▼
         git push origin main
              │
              ▼
┌─────────────────────────────────┐
│ GITHUB/GITLAB (Repositorio)  │
└─────────────┬───────────────┘
              │
              │ 4. SSH al VPS
              ▼
┌─────────────────────────────────┐
│ VPS (Producción/Test)        │
└─────────────┬───────────────┘
              │
              │ 5. Pull cambios
              ▼
         cd ~/projects/noa
         git pull origin main
              │
              │ 6. Reconstruir contenedores
              ▼
         docker-compose up -d --build
              │
              │ 7. Probar cambios
              ▼
         [Testing manual]
              └──► Repetir ciclo
```

### Comandos Rápidos del Workflow

**En el equipo local:**
```bash
# Verificar cambios
git status

# Commit rápido
git add .
git commit -m "feat: descripción breve"
git push origin main
```

**En el VPS (vía SSH):**
```bash
# Pull y rebuild
cd ~/projects/noa
git pull origin main
docker-compose up -d --build

# Verificar estado
docker-compose ps
docker-compose logs -f
```

---

## 🧪 Testing

### Test de Health Checks

```bash
# Test Evolution API
curl http://localhost:8080

# Test NOA Bot
curl http://localhost:2311/health
```

### Test de Flujo Conversacional

1. Enviar "Hola" al número de WhatsApp desde el teléfono
2. Verificar que el bot responda
3. Seguir el flujo completo:
   - Nombre → Industria → Redes → Problema
4. Verificar que el lead se envíe a n8n

### Test de Webhooks

```bash
# Simular mensaje de prueba
curl -X POST http://localhost:2311/api/v1/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "event": "messages.upsert",
    "data": {
      "key": {
        "remoteJid": "528442278408@s.whatsapp.net",
        "fromMe": false,
        "id": "test_001"
      },
      "message": {
        "conversation": "Test de webhook"
      }
    }
  }'
```

---

## 📝 Gestión de Contenedores

### Ver Logs

```bash
# Ver logs de Evolution API
docker-compose logs -f evolution-api

# Ver logs de NOA Bot
docker-compose logs -f noa-bot

# Ver logs de todos los servicios
docker-compose logs -f
```

### Reiniciar Servicios

```bash
# Reiniciar servicio específico
docker-compose restart evolution-api
docker-compose restart noa-bot

# Reiniciar todos
docker-compose restart
```

### Detener y Limpiar

```bash
# Detener todos los servicios
docker-compose down

# Detener y eliminar volumes (eliminará todos los datos)
docker-compose down -v

# Eliminar volumes específicos
docker volume rm noa_evolution_instances noa_evolution_uploads noa_evolution_db_data
```

---

## 🔍 Troubleshooting

### Problema: QR Code no se genera

**Síntomas:**
- Polling siempre devuelve `{"count": 0}`
- No aparece `base64` en la respuesta

**Solución:**
```bash
# Verificar logs de Evolution API
docker-compose logs evolution-api | tail -50

# Verificar estado de la instancia
curl -X GET http://localhost:8080/instance/fetchInstances \
  -H "apikey: TU_API_KEY"

# Recrear la instancia
curl -X DELETE http://localhost:8080/instance/delete/NOA_PROD \
  -H "apikey: TU_API_KEY"

# Volver a crear (ver Paso 1 de Configuración de WhatsApp)
```

### Problema: Conexión falla

**Solución:**
```bash
# Verificar acceso a internet
ping -c 3 google.com

# Verificar que el número esté activo
# Reiniciar Evolution API
docker-compose restart evolution-api

# Verificar logs
docker-compose logs -f evolution-api
```

### Problema: Webhook no funciona

**Solución:**
```bash
# Verificar webhook configurado
curl -X GET http://localhost:8080/webhook/find/NOA_PROD \
  -H "apikey: TU_API_KEY"

# Verificar que NOA Bot esté corriendo
docker-compose ps | grep noa-bot

# Verificar logs del bot
docker-compose logs noa-bot | tail -50
```

---

## 📊 Checklist Final de Configuración

### Configuración Local
- [ ] Archivo .env creado con placeholders
- [ ] Variables de entorno configuradas (sin valores reales en el repo)
- [ ] Contenedores levantados con `docker-compose up -d --build`
- [ ] Evolution API responde en puerto 8080
- [ ] NOA Bot responde en puerto 2311
- [ ] Instancia NOA_PROD creada
- [ ] QR code generado y escaneado
- [ ] Estado de instancia es "open"

### Configuración VPS
- [ ] SSH al VPS configurado
- [ ] Repositorio clonado en el VPS
- [ ] Archivo .env creado en el VPS
- [ ] Contenedores levantados en el VPS
- [ ] Instancia de WhatsApp configurada en el VPS
- [ ] Webhooks de n8n configurados

### Testing
- [ ] Health checks pasan
- [ ] Flujo conversacional funciona
- [ ] Leads se envían a n8n
- [ ] Logs no muestran errores

---

## 🔐 Notas de Seguridad

**IMPORTANTE:**
- NUNCA comitear archivos .env con API keys reales
- Usar .env.example como plantilla
- El archivo .env debe estar en .gitignore
- Reemplazar todos los valores sensibles con placeholders:
  - `TU_API_KEY_DE_EVOLUTION`
  - `sk-proj-TU_OPENAI_API_KEY_AQUI`
  - `https://flows.soul23.cloud/webhook/TU_WEBHOOK_ID`

---

## 📁 Archivos de Configuración

### .env.example
```bash
# OpenAI
OPENAI_API_KEY=sk-proj-tu-key-aqui

# Evolution API
EVOLUTION_API_URL=http://evolution-api:8080
EVOLUTION_API_TOKEN=tu-api-key-aqui
EVOLUTION_INSTANCE=NOA_PROD

# Webhooks de n8n
EXTERNAL_WEBHOOK_URL_PROD=https://flows.soul23.cloud/webhook/tu-webhook-id
EXTERNAL_WEBHOOK_URL_TEST=https://flows.soul23.cloud/webhook-test/tu-webhook-id

# Database
DATABASE_URL=sqlite:///./noa_dev.db
```

---

## ✅ Resumen

Esta guía proporciona:
1. Configuración local sin exponer información sensible
2. Configuración en VPS para despliegue
3. Flujo de trabajo Git (local → VPS)
4. Troubleshooting común
5. Checklist de configuración
6. Notas de seguridad

**🚀 Guía completa de configuración de NOA - Versión 1.0**
**Fecha:** 2024-01-31
