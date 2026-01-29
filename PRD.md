# PRD — NOA (Networked Operational Assistant)

## 1. Resumen

NOA es un asistente conversacional para WhatsApp diseñado para Noire Collective. Su función es calificar prospectos, recopilar información clave, analizar intención y sentimiento, recomendar servicios mediante RAG y escalar conversaciones a agentes humanos.

Opera mediante Evolution API + OpenAI + Base de Datos + Sistema RAG.

---

## 2. Objetivos del Producto

* Automatizar la primera fase de atención.
* Reducir carga operativa humana.
* Calificar leads.
* Recomendar servicios y planes adecuados.
* Centralizar datos de prospectos.
* Detectar riesgos y conflictos.
* Mejorar tasa de cierre.

---

## 3. Público Objetivo

* Emprendedores
* PYMES
* Negocios locales
* Marcas personales
* Proyectos digitales

---

## 4. Personalidad del Asistente

Nombre: NOA

Estilo:

* Profesional
* Directo
* Neutro
* Sin emojis
* Sin informalidad
* Orientado a resultados

---

## 5. Alcance Funcional

### Incluye

* Recepción de mensajes
* Gestión de estado conversacional
* Memoria persistente
* Análisis semántico
* Análisis de sentimiento
* Motor RAG
* Recomendaciones
* Escalamiento humano

### No Incluye

* Cierre de contratos
* Facturación
* Soporte postventa

---

## 6. Arquitectura General

WhatsApp ↓ Evolution API ↓ Webhook Backend (Python) ↓ OpenAI API ↓ RAG Engine ↓ Database ↓ Agente Humano

---

## 7. Flujo Conversacional Base

### Vista General

Secuencia obligatoria de captura → análisis → recomendación → escalamiento.

```
Inicio → Nombre → Giro → Redes → Problema → Análisis → Diagnóstico → Recomendación → (Humano | Cierre)
```

---

### Estado 0 — Inicio (INIT)

**Objetivo:** Explicar rol del asistente y preparar al usuario.

NOA: "Hola, soy NOA, asistente digital de Noire Collective. Te ayudaré a definir tu proyecto y prepararte para que un experto te atienda. Solo tomaré unos minutos. ¿Cuál es tu nombre?"

Entrada: Primer mensaje / sesión nueva Salida: nombre

---

### Estado 1 — Nombre (ASK_NAME)

**Objetivo:** Identificar al contacto.

NOA: "Gracias, {nombre}. ¿En qué giro o industria se encuentra tu negocio?"

Entrada: nombre Salida: giro

---

### Estado 2 — Giro (ASK_GIRO)

**Objetivo:** Clasificar industria.

NOA: "¿Con qué nombre aparece tu negocio en redes sociales o sitio web?"

Entrada: giro Salida: redes

---

### Estado 3 — Redes (ASK_REDES)

**Objetivo:** Validar presencia digital.

NOA: "Describe brevemente tu proyecto o problema actual."

Entrada: redes Salida: problema

---

### Estado 4 — Problema (ASK_PROBLEMA)

**Objetivo:** Capturar necesidad principal.

Proceso:

* Limpieza semántica
* Detección de intención
* Análisis de sentimiento

Entrada: problema Salida: texto procesado

---

### Estado 5 — Análisis y Diagnóstico (ANALYZE / DIAGNOSE)

**Objetivo:** Generar perfil del lead.

Proceso interno:

* LLM
* RAG
* Scoring
* Clasificación

Salida interna:

* Resumen
* Score
* Prioridad

---

### Estado 6 — Recomendación (RECOMMEND)

**Objetivo:** Proponer servicios y planes.

NOA: "Con base en tu proyecto, te recomiendo: {servicio} / {plan}."

Incluye:

* Justificación
* Alcance
* Beneficio principal

Salida: interés / objeción

---

### Estado 7 — Escalamiento (HANDOFF)

**Objetivo:** Transferir a humano.

Condición:

* Score alto
* Objeción crítica
* Ticket elevado
* Solicitud directa

NOA: "Te canalizo con un asesor para atención personalizada."

Acción: → Envío de resumen al agente

---

### Estado 8 — Cierre (CLOSED)

**Objetivo:** Finalizar sesión.

NOA: "Gracias. Un especialista continuará tu atención."

---

## 8. Datos Requeridos

```json
{
  "telefono": "",
  "nombre": "",
  "giro": "",
  "redes": "",
  "problema": "",
  "proyecto": "",
  "servicio_recomendado": "",
  "plan_recomendado": "",
  "sentimiento": "",
  "score_lead": 0,
  "fecha": ""
}
```

---

## 9. Base de Conocimiento (RAG)

### Fuentes

* Catálogo de servicios
* Planes
* Precios
* Casos de uso
* FAQs

### Indexación

* Embeddings
* Vector DB
* Metadata

---

## 10. Catálogo de Servicios

Incluye:

* Identidad Visual
* Creativos
* Flyers
* Tarjetas
* Banners
* Landing
* Web
* Ecommerce
* Bots
* Encuestas
* Producción
* Podcast
* Presentaciones
* Planes

Fuente: Base estructurada JSON

---

## 11. Motor de Recomendación

Criterios:

* Giro
* Presupuesto
* Objetivo
* Urgencia
* Madurez digital
* Capacidad operativa

Salida:

* Servicio principal
* Complementos
* Plan mensual

---

## 12. Análisis de Sentimiento

Clasificación:

* Positivo
* Neutral
* Negativo
* Riesgo

Triggers:

* Quejas
* Urgencia
* Amenaza
* Frustración

---

## 13. Escalamiento Humano

Condiciones:

* Solicitud directa
* Negativo/Riesgo
* Leads > 80
* Ticket > $10,000

Mensaje: "Te canalizo con un asesor para atención personalizada."

---

## 14. Scoring de Leads

Factores:

* Presupuesto
* Tamaño
* Claridad
* Urgencia
* Autoridad

Rango: 0–100

---

## 15. Seguridad

* Encriptación
* Tokens seguros
* Backups
* Logs
* Control de acceso

---

## 16. Métricas

* Conversión
* Escalamiento
* Tiempo medio
* Abandono
* Cierre

---

## 17. Prompt del Sistema (OpenAI)

Eres NOA, asistente profesional de Noire Collective.

Objetivo:

* Calificar
* Analizar
* Recomendar
* Escalar

Reglas:

* Directo
* Sin emojis
* No inventar
* Mantener contexto
* Priorizar datos

Flujo:

1. Nombre
2. Giro
3. Redes
4. Problema
5. Diagnóstico
6. Recomendación
7. Escalar

---

## 18. Roadmap

Fase 1: MVP Fase 2: RAG Fase 3: CRM Fase 4: BI Fase 5: Multi-agente

---

## 19. Riesgos

* Baja calidad de leads
* Errores de contexto
* Costos API
* Saturación humana

---

## 20. Definición de Éxito

* +40% conversión
* -60% carga humana
* +30% ticket medio
* +25% retención

---

## 21. Stack Tecnológico

### Backend

* Python 3.11+
* FastAPI
* Uvicorn

### Integraciones

* Evolution API (WhatsApp)
* OpenAI API (LLM + Embeddings)
* Webhooks REST

### Base de Datos

* PostgreSQL (producción)
* SQLite (desarrollo)
* Redis (cache de sesiones)

### RAG

* FAISS / ChromaDB
* OpenAI Embeddings
* Metadata Store

### Infraestructura

* Docker
* Docker Compose
* VPS (Linux)
* Nginx

---

## 22. Estructura del Proyecto

```
noa-bot/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── routes/
│   ├── services/
│   │   ├── openai.py
│   │   ├── rag.py
│   │   ├── sentiment.py
│   │   └── recommender.py
│   ├── db/
│   │   ├── models.py
│   │   └── session.py
│   └── flows/
│       └── states.py
├── data/
│   └── services.json
├── vectorstore/
├── logs/
└── docker-compose.yml
```

---

## 23. Modelo de Estados Conversacionales con Diálogos y Objeciones

Estados Finite State Machine (FSM):

### INIT / ASK_NAME

**Objetivo:** Iniciar relación y capturar nombre.

NOA: "Hola, soy NOA, asistente digital de Noire Collective. Te ayudaré a definir tu proyecto y prepararte para que un experto te atienda. ¿Cuál es tu nombre?"

Objeción: "¿Para qué necesitas mi nombre?" Respuesta: "Para personalizar la atención y asignarte un asesor adecuado."

---

### ASK_GIRO

**Objetivo:** Identificar industria.

NOA: "Gracias, {nombre}. ¿En qué ramo se encuentra tu negocio?"

Objeción: "Es variado / no sé" Respuesta: "Indícame la actividad principal que genera más ingresos."

---

### ASK_REDES

**Objetivo:** Validar presencia digital.

NOA: "¿Con qué nombre apareces en redes sociales o sitio web?"

Objeción: "No tengo redes" Respuesta: "Perfecto. Lo tomamos como oportunidad de crecimiento."

---

### ASK_PROBLEMA

**Objetivo:** Detectar necesidad principal.

NOA: "Describe brevemente tu objetivo o problema principal."

Objeción: "Quiero todo" Respuesta: "Indícame qué es lo más urgente ahora mismo."

---

### ANALYZE

**Objetivo:** Procesar contexto, sentimiento y scoring.

NOA: "Estoy analizando tu información."

(Proceso interno: LLM + RAG + scoring)

---

### RECOMMEND

**Objetivo:** Proponer solución.

NOA: "Con base en tu proyecto, te recomiendo: {servicio} / {plan}."

Objeción: "Está caro" Respuesta: "La propuesta está basada en impacto y retorno. También podemos ajustar alcance."

Objeción: "Lo voy a pensar" Respuesta: "Te asigno un asesor para resolver dudas antes de decidir."

Objeción: "Solo quiero algo pequeño" Respuesta: "Podemos iniciar con una versión mínima y escalar después."

---

### HANDOFF

**Objetivo:** Transferir a humano.

NOA: "Te canalizo con un asesor para atención personalizada."

Acción: → Envío de resumen al agente.

---

### CLOSED

**Objetivo:** Cerrar interacción.

NOA: "Gracias. Un especialista continuará tu atención."

---

Estados Finite State Machine (FSM):

* INIT
* ASK_NAME
* ASK_GIRO
* ASK_REDES
* ASK_PROBLEMA
* ANALYZE
* RECOMMEND
* HANDOFF
* CLOSED

Cada usuario mantiene un estado persistente.

---

## 24. Diagramas de Flujo

### Flujo General

```
Usuario → WhatsApp → Evolution → Backend
        → FSM → OpenAI → RAG → DB
        → Respuesta → Usuario
```

### Flujo Conversacional

```
Inicio
  ↓
Nombre
  ↓
Giro
  ↓
Redes
  ↓
Problema
  ↓
Análisis
  ↓
Recomendación
  ↓
¿Humano?
  ├─ Sí → Agente
  └─ No → Cierre
```

---

## 25. Diálogos Operativos Completos

### Bienvenida

"Hola, soy NOA, asistente digital de Noire Collective. Te ayudaré a definir tu proyecto y prepararte para que un experto te atienda. ¿Cuál es tu nombre?"

### Solicitud Giro

"Gracias, {nombre}. ¿En qué ramo se encuentra tu negocio?"

### Solicitud Redes

"¿Con qué nombre apareces en redes sociales o sitio web?"

### Solicitud Problema

"Describe brevemente tu objetivo o problema principal."

### Diagnóstico

"Estoy analizando tu información para recomendarte la mejor opción."

### Recomendación

"Con base en tu proyecto, te recomiendo: {servicio} / {plan}."

### Escalamiento

"Te canalizo con un asesor para atención personalizada."

### Cierre

"Gracias. Un especialista continuará tu atención."

---

## 26. Lógica RAG

### Pipeline

1. Normalización de consulta
2. Embedding
3. Similarity Search
4. Filtrado por metadata
5. Context Injection
6. Respuesta LLM

---

## 27. Gestión de Memoria

Tipos:

* Corto plazo (Redis)
* Largo plazo (DB)
* Vectorial (RAG)

Persistencia por teléfono.

---

## 28. Motor de Decisión

Reglas:

IF score > 80 AND ticket > 10000 → HANDOFF IF sentimiento = negativo → HANDOFF IF pregunta = técnica → RAG IF duda simple → LLM

---

## 29. Manejo de Errores

* Timeout API
* Fallo LLM
* Mensaje inválido
* Contexto corrupto

Fallback: Derivación humana.

---

## 30. Deployment

Proceso:

1. Build Docker
2. Push registry
3. Deploy VPS
4. Run migrations
5. Load vectors
6. Start services

---

## 31. Versionado

v1.0 — MVP v1.1 — RAG v1.2 — CRM v2.0 — Multiagente
