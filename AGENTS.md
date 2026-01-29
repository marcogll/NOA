# AGENTS.md - Guía para Agentes de IA (NOA Developer)

Este documento proporciona instrucciones y contexto para los agentes de IA que trabajen en el desarrollo y mantenimiento de NOA (Networked Operational Assistant).

## Contexto del Proyecto
NOA es un asistente conversacional para WhatsApp diseñado para Noire Collective. Su función principal es calificar prospectos, analizar intención y sentimiento, y recomendar servicios mediante un motor RAG, escalando a agentes humanos cuando sea necesario.

## Personalidad y Estilo (Sección 4 PRD)
Al desarrollar o interactuar como NOA, se deben seguir estas directrices:
- **Profesional**: Mantener un tono corporativo y serio.
- **Directo**: Ir al grano, sin rodeos.
- **Neutro**: No mostrar sesgos emocionales.
- **Sin emojis**: No utilizar emoticonos en ninguna comunicación.
- **Sin informalidad**: Evitar modismos o lenguaje casual.
- **Orientado a resultados**: Focarse en completar el flujo y obtener datos.

## Stack Tecnológico (Sección 21 PRD)
Los agentes deben estar familiarizados con:
- **Backend**: Python 3.11+, FastAPI, Uvicorn.
- **Integraciones**: Evolution API (WhatsApp), OpenAI API (LLM + Embeddings).
- **Base de Datos**: PostgreSQL (producción), SQLite (desarrollo), Redis (cache).
- **RAG**: FAISS / ChromaDB, OpenAI Embeddings.
- **Infraestructura**: Docker, Docker Compose, VPS (Linux).

## Arquitectura de Conversación (Sección 23 PRD)
NOA utiliza una **Finite State Machine (FSM)** para la gestión de estados:
1. **INIT**: Bienvenida y captura de nombre.
2. **ASK_NAME**: Identificación del contacto.
3. **ASK_GIRO**: Identificación de la industria.
4. **ASK_REDES**: Validación de presencia digital.
5. **ASK_PROBLEMA**: Captura de necesidad principal.
6. **ANALYZE**: Procesamiento de contexto, sentimiento y scoring.
7. **RECOMMEND**: Propuesta de servicio/plan.
8. **HANDOFF**: Transferencia a humano.
9. **CLOSED**: Cierre de sesión.

## Instrucciones de Desarrollo
- **Código**: Seguir estándares PEP 8.
- **Documentación**: Documentar funciones y servicios críticos.
- **Seguridad**: No exponer tokens o claves en el código; usar variables de entorno.
- **Flujos**: Asegurar que cada transición de estado esté correctamente validada en la FSM.
