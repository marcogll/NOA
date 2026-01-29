from openai import AsyncOpenAI
from app.config import settings
import json

class OpenAIService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def analyze_text(self, text: str):
        """
        Analyzes the user's text to extract intent, sentiment, and basic info.
        For now, returns a simple placeholder analysis.
        """
        if not settings.OPENAI_API_KEY:
            return {"sentiment": "neutral", "intent": "unknown", "score": 50}

        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are NOA, a professional assistant. Analyze the user's message for sentiment, intent, and lead score (0-100). Respond only in JSON."},
                    {"role": "user", "content": text}
                ],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            # Fallback for errors
            return {"sentiment": "neutral", "intent": "error", "score": 0, "error": str(e)}

openai_service = OpenAIService()
