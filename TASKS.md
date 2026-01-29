# TASKS.md - Listado de Tareas para el Desarrollo de NOA

Este documento organiza las tareas necesarias para cumplir con el Roadmap y los objetivos definidos en el PRD.

## Fase 1: MVP (Mínimo Producto Viable)
- [ ] **Configuración Inicial**
  - [ ] Crear estructura de directorios siguiendo `noa-bot/` definido en el PRD (Sección 22).
  - [ ] Configurar entorno virtual y `requirements.txt`.
  - [ ] Configurar Docker y Docker Compose básico.
- [ ] **Backend Base**
  - [ ] Implementar servidor FastAPI (`app/main.py`).
  - [ ] Configurar manejo de variables de entorno (`app/config.py`).
  - [ ] Configurar logs y manejo de errores globales.
- [ ] **Conversación y Estados (FSM)**
  - [ ] Implementar motor de estados en `app/flows/states.py`.
  - [ ] Definir lógica de transición para los estados: INIT, ASK_NAME, ASK_GIRO, ASK_REDES, ASK_PROBLEMA.
- [ ] **Integración WhatsApp**
  - [ ] Implementar servicio para Evolution API.
  - [ ] Configurar Webhook para recepción de mensajes.
- [ ] **Análisis de OpenAI**
  - [ ] Implementar servicio de OpenAI (`app/services/openai.py`).
  - [ ] Configurar Prompt del Sistema (Sección 17 PRD).
  - [ ] Implementar detección de intención y extracción de datos básicos.
- [ ] **Persistencia**
  - [ ] Configurar base de datos SQLite para desarrollo.
  - [ ] Crear modelos de datos para Leads y Sesiones.

## Fase 2: RAG y Recomendación
- [ ] **Motor RAG**
  - [ ] Implementar servicio de RAG (`app/services/rag.py`).
  - [ ] Configurar base de datos vectorial (FAISS/ChromaDB).
  - [ ] Indexar catálogo de servicios y planes (JSON).
- [ ] **Diagnóstico y Recomendación**
  - [ ] Implementar lógica de análisis y diagnóstico (`ANALYZE`).
  - [ ] Implementar motor de recomendación de servicios (`RECOMMEND`).
- [ ] **Análisis Avanzado**
  - [ ] Implementar análisis de sentimiento (`app/services/sentiment.py`).
  - [ ] Implementar scoring de leads (`Sección 14 PRD`).

## Fase 3: Escalamiento y CRM
- [ ] **Escalamiento Humano**
  - [ ] Implementar lógica de transferencia (`HANDOFF`).
  - [ ] Configurar notificaciones a agentes humanos según el score.
- [ ] **Integración CRM**
  - [ ] Sincronizar datos de leads capturados con sistema externo.
- [ ] **Persistencia de Producción**
  - [ ] Migrar a PostgreSQL.
  - [ ] Configurar Redis para gestión de sesiones.

## Fase 4: BI y Optimización
- [ ] **Métricas y BI**
  - [ ] Implementar recolección de métricas de conversión y tiempos.
  - [ ] Crear reportes básicos de rendimiento del bot.
- [ ] **Seguridad**
  - [ ] Auditoría de tokens y logs.
  - [ ] Implementar backups automáticos.

## Fase 5: Multi-agente
- [ ] **Soporte Multi-instancia**
  - [ ] Adaptar arquitectura para manejar múltiples números/clientes.
