from openai import AsyncOpenAI
from app.config import settings
import json


class SentimentService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def analyze_sentiment(self, text: str):
        """
        Analyzes sentiment using OpenAI API.
        Returns: 'positive', 'neutral', or 'negative'
        """
        if not settings.OPENAI_API_KEY:
            return "neutral"

        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Analiza el sentimiento del texto y responde únicamente con: 'positive', 'neutral', o 'negative'.",
                    },
                    {"role": "user", "content": text},
                ],
                max_tokens=10,
                temperature=0,
            )
            sentiment = response.choices[0].message.content.strip().lower()
            return (
                sentiment
                if sentiment in ["positive", "neutral", "negative"]
                else "neutral"
            )
        except Exception as e:
            # Fallback for errors
            return "neutral"


sentiment_service = SentimentService()
