# NOA - Networked Operational Assistant

NOA es un asistente conversacional inteligente para WhatsApp, diseñado para Noire Collective. Su objetivo es automatizar la calificación de leads, analizar el sentimiento de los prospectos y recomendar servicios específicos mediante un motor RAG (Retrieval-Augmented Generation).

## 🚀 Características Principales

- **Gestión de Estados (FSM)**: Flujo conversacional estructurado para guiar al usuario desde el inicio hasta el diagnóstico.
- **Análisis de IA**: Detección de intención, extracción de datos y análisis de sentimiento mediante OpenAI GPT.
- **Motor RAG**: Recomendaciones personalizadas basadas en el catálogo de servicios de la empresa.
- **Integración con WhatsApp**: Comunicación en tiempo real a través de Evolution API.
- **Scoring de Leads**: Calificación automática de prospectos para priorizar la atención humana.
- **Etiquetado Automático**: Organización de contactos en WhatsApp mediante tags basados en su estado y score.

## 🛠️ Stack Tecnológico

- **Lenguaje**: Python 3.11+
- **Framework Web**: FastAPI
- **LLM**: OpenAI API (GPT-4 & Embeddings)
- **Mensajería**: Evolution API (WhatsApp)
- **Bases de Datos**:
  - PostgreSQL (Persistencia de datos)
  - Redis (Gestión de sesiones/caché)
  - FAISS / ChromaDB (Almacenamiento vectorial)
- **Infraestructura**: Docker & Docker Compose

## 📁 Estructura del Proyecto

```text
noa-bot/
├── app/
│   ├── main.py            # Punto de entrada de la aplicación
│   ├── config.py          # Configuración y variables de entorno
│   ├── routes/            # Endpoints y Webhooks
│   ├── services/          # Integraciones (OpenAI, RAG, Evolution API)
│   ├── db/                # Modelos y sesión de base de datos
│   └── flows/             # Lógica de la FSM (estados conversacionales)
├── data/                  # Catálogo de servicios y archivos JSON
├── vectorstore/           # Índices vectoriales para RAG
├── logs/                  # Registros del sistema
└── docker-compose.yml     # Orquestación de contenedores
```

## 📖 Documentación Relacionada

Para más detalles sobre el proyecto, consulta los siguientes documentos:

- [**PRD.md**](./PRD.md): Requerimientos detallados del producto.
- [**AGENTS.md**](./AGENTS.md): Guía específica para el desarrollo con agentes de IA.
- [**SKILLS.md**](./SKILLS.md): Habilidades técnicas y de dominio requeridas.
- [**TASKS.md**](./TASKS.md): Roadmap y listado de tareas pendientes.

## ⚙️ Configuración Rápida

1. **Clonar el repositorio**:
   ```bash
   git clone <repo-url>
   cd noa-bot
   ```

2. **Configurar variables de entorno**:
   Crea un archivo `.env` basado en la documentación técnica con tus claves de OpenAI y Evolution API.

3. **Desplegar con Docker**:
   ```bash
   docker-compose up -d --build
   ```

---
Desarrollado para **Noire Collective**.
