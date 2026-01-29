# PRD — NOA (Networked Operational Assistant)

## I. RESUMEN Y OBJETIVOS

NOA es un asistente conversacional avanzado para WhatsApp diseñado para **Noire Collective**. Su propósito principal es automatizar la fase inicial de atención al cliente, calificando prospectos y ofreciendo recomendaciones personalizadas mediante Inteligencia Artificial.

### Objetivos Principales:
- **Automatización**: Gestionar el primer contacto sin intervención humana.
- **Calificación (Lead Scoring)**: Identificar prospectos de alto valor.
- **Personalización**: Recomendar servicios específicos mediante un motor RAG.
- **Escalamiento Inteligente**: Transferir a agentes humanos solo cuando sea necesario o el valor del lead lo justifique.
- **Eficiencia Operativa**: Reducir la carga de trabajo manual y mejorar la tasa de conversión.

---

## II. PÚBLICO OBJETIVO Y PERSONALIDAD

### Público Objetivo:
- Emprendedores, PYMES y negocios locales.
- Marcas personales y proyectos digitales.

### Personalidad de NOA:
- **Nombre**: NOA
- **Estilo**: Profesional, directo y neutro.
- **Restricciones**: No utiliza emojis, no usa lenguaje informal, mantiene un enfoque estrictamente orientado a resultados.

---

## III. ESPECIFICACIONES FUNCIONALES

### Alcance (Incluye):
- Recepción de mensajes y gestión de estados conversacionales (FSM).
- Análisis semántico y de sentimiento.
- Recomendación de servicios basada en catálogo (RAG).
- **Etiquetado automático** de contactos en WhatsApp según estado y score.
- Escalamiento a agentes humanos bajo condiciones específicas.

### Fuera de Alcance:
- Cierre formal de contratos y facturación.
- Soporte postventa detallado.

---

## IV. ARQUITECTURA TÉCNICA Y STACK

### Flujo de Arquitectura:
`WhatsApp (Evolution API) ↔ Webhook Backend (FastAPI) ↔ OpenAI API ↔ RAG Engine ↔ DB`

### Stack Tecnológico:
- **Backend**: Python 3.11+, FastAPI, Uvicorn.
- **IA**: OpenAI API (GPT-4 para lógica, Embeddings para RAG).
- **Bases de Datos**: PostgreSQL (Producción), SQLite (Desarrollo), Redis (Caché de sesiones).
- **RAG**: FAISS / ChromaDB como almacén vectorial.
- **Infraestructura**: Docker, Docker Compose, Nginx, VPS Linux.

### Estructura del Proyecto:
```text
noa-bot/
├── app/
│   ├── main.py, config.py
│   ├── routes/ (webhooks)
│   ├── services/ (openai, rag, sentiment, recommender)
│   ├── db/ (models, session)
│   └── flows/ (states)
├── data/ (services.json)
├── vectorstore/ (faiss_index)
└── docker-compose.yml
```

---

## V. LÓGICA CONVERSACIONAL Y ESTADOS (FSM)

NOA opera mediante una **Máquina de Estados Finitos (FSM)** para garantizar un flujo consistente:

1.  **INIT / ASK_NAME**: Saludo inicial y captura de nombre.
2.  **ASK_GIRO**: Identificación del ramo o industria.
3.  **ASK_REDES**: Validación de presencia digital.
4.  **ASK_PROBLEMA**: Descripción de la necesidad u objetivo principal.
5.  **ANALYZE**: Procesamiento interno (Intención, Sentimiento, Scoring).
6.  **RECOMMEND**: Presentación de propuesta basada en el catálogo (RAG).
7.  **HANDOFF**: Transferencia a asesor humano si se cumplen los criterios.
8.  **CLOSED**: Finalización de la interacción.

### Manejo de Objeciones:
- El asistente cuenta con respuestas predefinidas para objeciones sobre privacidad (nombre), costo de servicios y dudas técnicas iniciales.

---

## VI. INTELIGENCIA ARTIFICIAL Y NEGOCIO

### Motor RAG (Retrieval-Augmented Generation):
- **Proceso**: Normalización → Embedding → Búsqueda de Similitud → Inyección de Contexto → Respuesta Generada.
- **Fuente**: Catálogo estructurado de servicios, planes y precios en JSON.

### Análisis y Calificación:
- **Sentimiento**: Clasificación (Positivo, Neutral, Negativo, Riesgo).
- **Lead Scoring (0-100)**: Basado en presupuesto, claridad de objetivos, urgencia y autoridad del contacto.

### Prompt del Sistema:
- "Eres NOA, asistente profesional de Noire Collective. Objetivo: Calificar, analizar, recomendar y escalar. Reglas: Directo, sin emojis, no inventar datos, mantener el contexto."

---

## VII. GESTIÓN DE DATOS Y ESCALAMIENTO

### Datos Requeridos:
- Teléfono, nombre, giro, redes, problema, servicio/plan recomendado, sentimiento, score y **timestamp (siempre en formato UTC)**.

### Etiquetado en WhatsApp (Tags):
Uso de Evolution API para asignar etiquetas automáticas:
- `Lead-Nuevo`, `Lead-Calificado`, `Lead-Prioridad-Alta`, `Requiere-Humano`.

### Criterios de Escalamiento Humano:
- Solicitud directa del usuario.
- Detección de sentimiento negativo o riesgo.
- Lead Score > 80.
- Valor potencial de ticket > $10,000.

---

## VIII. SEGURIDAD Y OPERACIONES

- **Seguridad**: Encriptación de datos, gestión segura de tokens mediante variables de entorno, control de acceso mediante logs detallados.
- **Manejo de Errores**: Fallback automático a transferencia humana si el motor de IA o las APIs externas fallan.
- **Despliegue**: Proceso automatizado con Docker; migraciones de base de datos y carga de vectores iniciales.

---

## IX. ROADMAP Y MÉTRICAS DE ÉXITO

### Roadmap:
1.  **Fase 1 (MVP)**: Flujo de conversación básico y estados.
2.  **Fase 2 (RAG)**: Integración de catálogo y recomendaciones inteligentes.
3.  **Fase 3 (CRM & Etiquetas)**: Sincronización externa y etiquetado avanzado.
4.  **Fase 4 (BI & Analytics)**: Dashboards de métricas y optimización de prompts.
5.  **Fase 5 (Multi-agente)**: Soporte para múltiples instancias y departamentos.

### Definición de Éxito:
- Incremento del 40% en la tasa de conversión.
- Reducción del 60% en la carga de atención inicial humana.
- Mejora en la precisión de las recomendaciones de servicio.

---
**Versión**: 1.1
**Última Actualización**: Timestamp UTC actual
