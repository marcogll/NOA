# NOA - Testing Guide

## 🧪 Tests Configurados

### Tests Unitarios
```bash
# Ejecutar todos los tests
pytest tests/ -v

# Tests específicos de webhooks
pytest tests/test_webhooks.py -v

# Tests con coverage
pytest tests/ --cov=app --cov-report=html
```

### Tests Manuales para Hoy

#### 1. Test de Webhook (Postman/curl)
```bash
curl -X POST http://localhost:2311/api/v1/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "event": "messages.upsert",
    "data": {
      "key": {
        "remoteJid": "528442278408@s.whatsapp.net",
        "fromMe": false,
        "id": "test_msg_001"
      },
      "message": {
        "conversation": "Hola, quiero información"
      }
    }
  }'
```

#### 2. Test de Flujo Completo
1. **Estado INIT → ASK_NAME**: Enviar "hola"
2. **ASK_NAME → ASK_INDUSTRY**: Enviar nombre
3. **ASK_INDUSTRY → ASK_SOCIAL_MEDIA**: Enviar industria
4. **ASK_SOCIAL_MEDIA → ASK_PROBLEM**: Enviar redes sociales
5. **ASK_PROBLEM → ANALYZE**: Enviar problema
6. **CHECK**: Verificar webhook externo reciba data

#### 3. Test de Webhooks Externos (n8n)

**Nota:** Las URLs de webhooks de n8n se configuran en el archivo .env del proyecto (ver .env.example). Los IDs específicos se obtienen desde tu instancia de n8n.

**Verificación de conectividad:**
```bash
# Reemplazar TU_WEBHOOK_ID con el ID real de tu workflow de n8n
curl https://flows.soul23.cloud/webhook/TU_WEBHOOK_ID_PRODUCCION
curl https://flows.soul23.cloud/webhook-test/TU_WEBHOOK_ID_TEST
```

#### 4. Validaciones
- JSON inválido → 400
- Evento inválido → 400
- Teléfono inválido → 400
- Sin texto → "no_text"
- Mensaje propio → "ignored_from_me"

## 🔍 Checklist de Testing

### Funcionalidad Básica
- [ ] Inicia conversación correctamente
- [ ] Transiciona entre estados
- [ ] Responde en español con emojis
- [ ] Guarda datos en PostgreSQL
- [ ] Envía a webhooks duales

### Análisis de IA
- [ ] Analiza sentimiento
- [ ] Calcula lead score
- [ ] Recomienda servicio correcto
- [ ] Usa data real de services.json

### Validación
- [ ] Rechaza payloads inválidos
- [ ] Maneja errores gracefully
- [ ] Rate limiting (si implementado)

### Performance
- [ ] Respuesta < 3 segundos
- [ ] Sin memory leaks
- [ ] Conexiones DB manejadas

## 📊 Results Esperados

### Lead Score Thresholds
- **≥70**: Planes Premium (Gold/Black)
- **≥40**: Planes Medium (Silver) o servicios especiales
- **<40**: Planes Básicos o servicios individuales

### Webhook Payload Verificación
```json
{
  "uuid": "uuid-único",
  "timestamp": "2024-01-29T18:30:00Z",
  "source": "NOA_BOT",
  "instance": "NOA_PROD",
  "data": {
    "phone": "+528442278408",
    "name": "capturado",
    "industry": "capturado",
    "social_media": "capturado",
    "problem": "capturado",
    "sentiment": "positive/neutral/negative",
    "intent": "detected",
    "lead_score": 85,
    "recommended_service": "de catálogo",
    "state": "CLOSED"
  }
}
```

**Nota:** El nombre de instancia se configura en el archivo .env (EVOLUTION_INSTANCE).

## 🚨 Issues a Monitor

### Comunes
1. **Timeout de OpenAI**: Verificar API key
2. **Webhook externo caído**: Reintentos automáticos
3. **PostgreSQL connection**: Pool agotado
4. **Invalid phone format**: Validación regex

### Logs Importantes
- `logger.error()` para errores críticos
- `logger.warning()` para validaciones
- `logger.info()` para webhook envíos

---

**Ready para testing this afternoon! 🎯**