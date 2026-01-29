from openai import AsyncOpenAI
from app.config import settings
import json
import os


class RAGService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        # Load real services and plans data
        self.services_data = self._load_services_data()
        self.plans_data = self._load_plans_data()

    def _load_services_data(self):
        """Load services from JSON file"""
        try:
            with open(
                "/home/marco/Work/code/NOA/data/services.json", "r", encoding="utf-8"
            ) as f:
                return json.load(f)
        except Exception:
            return {"services": []}

    def _load_plans_data(self):
        """Load plans from JSON file"""
        try:
            with open(
                "/home/marco/Work/code/NOA/data/plan.json", "r", encoding="utf-8"
            ) as f:
                content = f.read()
                # Remove markdown code block markers if present
                if content.startswith("```json"):
                    content = content[7:]
                if content.endswith("```"):
                    content = content[:-3]
                return json.loads(content.strip())
        except Exception:
            return {"plans": []}

    async def search_context(self, query: str, lead_info: dict = None):
        """
        Recommends services and plans based on user query and lead information
        """
        if not settings.OPENAI_API_KEY or not lead_info:
            return self._get_default_recommendation()

        try:
            # Create context from user info
            context = f"""
            Usuario: {lead_info.get("name", "Unknown")}
            Industria: {lead_info.get("industry", "Unknown")}
            Problema: {lead_info.get("problem", "Unknown")}
            Sentimiento: {lead_info.get("sentiment", "Unknown")}
            Puntuación: {lead_info.get("lead_score", 50)}
            """

            services_text = json.dumps(self.services_data, ensure_ascii=False)
            plans_text = json.dumps(self.plans_data, ensure_ascii=False)

            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"""
                    Eres un asistente de Noire Collective. Analiza la información del usuario y recomienda la mejor opción entre servicios individuales o planes mensuales.
                    
                    SERVICIOS DISPONIBLES:
                    {services_text}
                    
                    PLANES DISPONIBLES:
                    {plans_text}
                    
                    Basado en la puntuación del lead:
                    - Si score >= 70: Recomienda plan "Black" o "Gold"
                    - Si score >= 40: Recomienda plan "Silver" o servicio especial
                    - Si score < 40: Recomienda plan "Básico" o servicio individual
                    
                    Responde únicamente con JSON con este formato:
                    {{
                        "type": "service" o "plan",
                        "name": "nombre del servicio/plan",
                        "description": "descripción completa",
                        "price": "precio en formato $X o $X/mes",
                        "category": "categoría",
                        "details": "detalles adicionales"
                    }}
                    """,
                    },
                    {
                        "role": "user",
                        "content": f"Contexto: {context}\n\nConsulta: {query}",
                    },
                ],
                response_format={"type": "json_object"},
                temperature=0.3,
            )

            content = response.choices[0].message.content
            recommended = json.loads(content) if content else {}

            # Validate response contains required fields
            if all(key in recommended for key in ["name", "description", "price"]):
                return recommended
            else:
                return self._get_default_recommendation()

        except Exception as e:
            # Fallback to default recommendation
            return self._get_default_recommendation()

    def _get_default_recommendation(self):
        """Default recommendation for errors or missing API key"""
        return {
            "type": "plan",
            "name": "Silver",
            "description": "10 diseños gráficos, 7 videos, 1 campaña pagada (30 días), 45 min de respuesta a comentarios, 10 historias.",
            "price": "$3,800/mes",
            "category": "Planes",
            "details": "Plan balanceado para crecimiento digital",
        }


rag_service = RAGService()
