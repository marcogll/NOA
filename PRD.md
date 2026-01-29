# PRD — NOA (Networked Operational Assistant)

## 1. Resumen y Objetivos

NOA es un asistente conversacional para WhatsApp diseñado para Noire Collective. Su función es automatizar la primera fase de atención al cliente, calificando prospectos y recomendando servicios mediante IA.

### Objetivos:
* Automatizar la calificación de leads.
* Reducir la carga operativa humana.
* Recomendar servicios y planes adecuados mediante RAG.
* Centralizar datos de prospectos y detectar riesgos/conflictos.
* Mejorar la tasa de cierre y el ticket medio.

---

## 2. Público Objetivo

* Emprendedores y PYMES.
* Negocios locales y marcas personales.
* Proyectos digitales que buscan profesionalizar su atención.

---

## 3. Personalidad del Asistente

* **Nombre**: NOA
* **Estilo**: Profesional, directo, neutro.
* **Restricciones**: Sin emojis, sin informalidad, orientado estrictamente a resultados.

---

## 4. Alcance del Proyecto

### Incluye:
* Recepción de mensajes y gestión de estado (FSM).
* Análisis semántico, de sentimiento y motor RAG.
* Recomendaciones de servicios y scoring de leads.
* Etiquetado automático en WhatsApp y escalamiento humano.

### No Incluye:
* Cierre de contratos o facturación.
* Soporte postventa.

---

## 5. Arquitectura y Stack Tecnológico

### Flujo de Datos:
WhatsApp (Evolution API) ↔ Webhook Backend (Python/FastAPI) ↔ OpenAI API ↔ RAG Engine ↔ Base de Datos.

### Stack:
* **Backend**: Python 3.11+, FastAPI, Uvicorn.
* **IA**: OpenAI API (LLM + Embeddings).
* **Bases de Datos**: PostgreSQL (Pro), SQLite (Dev), Redis (Cache de sesiones).
* **RAG**: FAISS / ChromaDB + OpenAI Embeddings.
* **Infraestructura**: Docker, Docker Compose, Nginx, VPS Linux.

### Estructura del Proyecto:
```text
noa-bot/
├── app/
│   ├── main.py, config.py
│   ├── routes/, services/ (openai, rag, sentiment, recommender)
│   ├── db/ (models, session)
│   └── flows/ (states)
├── data/ (services.json), vectorstore/
└── docker-compose.yml
```

---

## 6. Flujo Conversacional y Modelo de Estados (FSM)

### Estados de la FSM:
1. **INIT / ASK_NAME**: Bienvenida y captura de nombre.
2. **ASK_GIRO**: Identificación de industria.
3. **ASK_REDES**: Validación de presencia digital.
4. **ASK_PROBLEMA**: Captura de necesidad principal.
5. **ANALYZE**: Procesamiento de contexto, sentimiento y scoring.
6. **RECOMMEND**: Propuesta de solución basada en RAG.
7. **HANDOFF**: Transferencia a agente humano (si aplica).
8. **CLOSED**: Cierre de sesión.

### Manejo de Objeciones:
* **"¿Para qué el nombre?"**: "Para personalizar la atención y asignarte un asesor adecuado."
* **"Está caro"**: "La propuesta se basa en impacto y retorno; podemos ajustar el alcance."

---

## 7. Componentes de Inteligencia y Lógica de Negocio

### Motor RAG:
Pipeline: Normalización → Embedding → Similarity Search → Filtrado → Inyección de Contexto → Respuesta.
Fuentes: Catálogo de servicios, planes, precios y FAQs (data/services.json).

### Análisis y Scoring:
* **Sentimiento**: Clasificación en Positivo, Neutral, Negativo o Riesgo (Triggers: quejas, urgencia).
* **Scoring (0-100)**: Basado en presupuesto, tamaño, claridad, urgencia y autoridad.

### Prompt del Sistema:
"Eres NOA, asistente profesional de Noire Collective. Objetivo: Calificar, analizar, recomendar y escalar. Reglas: Directo, sin emojis, no inventar, mantener contexto."

---

## 8. Datos, Memoria y Escalamiento

### Datos Capturados:
Teléfono, nombre, giro, redes, problema, servicio/plan recomendado, sentimiento, score y timestamp (siempre en formato UTC).

### Gestión de Etiquetas (WhatsApp Tags):
El sistema debe etiquetar automáticamente al contacto en WhatsApp mediante Evolution API según su estado:
* `Lead-Nuevo`, `Lead-Calificado`, `Lead-Prioridad-Alta`, `Requiere-Humano`.

### Escalamiento Humano:
Condiciones: Solicitud directa, sentimiento de riesgo, score > 80 o ticket > $10,000.

---

## 9. Seguridad, Métricas y Operaciones

### Seguridad:
Encriptación, tokens seguros, backups automáticos y control de acceso por logs.

### Métricas de Éxito:
* +40% conversión.
* -60% carga operativa humana.
* +30% ticket medio.

### Manejo de Errores:
Fallback a derivación humana en caso de fallos en la API de OpenAI o tiempos de espera agotados.

---

## 10. Roadmap y Versionado

* **Fase 1 (MVP)**: Flujo básico, FSM e integración con WhatsApp.
* **Fase 2 (RAG)**: Implementación de motor vectorial y recomendaciones.
* **Fase 3 (CRM)**: Integración con sistemas externos y escalamiento avanzado.
* **Fase 4 (BI)**: Dashboards de métricas y optimización de prompts.
* **Fase 5 (Multi-agente)**: Soporte para múltiples instancias y departamentos.

**Versión Actual**: v1.0 (MVP)
