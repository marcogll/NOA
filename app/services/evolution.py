import httpx
from app.config import settings
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


class EvolutionService:
    def __init__(self):
        self.base_url = settings.EVOLUTION_API_URL
        self.api_key = settings.EVOLUTION_API_TOKEN
        self.instance = settings.EVOLUTION_INSTANCE
        self.headers = {"apikey": self.api_key, "Content-Type": "application/json"}

    async def send_message(self, number: str, text: str):
        # Try to send real message first, fall back to simulation
        try:
            url = f"{self.base_url}/message/sendText/{self.instance}"
            payload = {
                "number": number,
                "options": {"delay": 1200, "presence": "composing"},
                "text_message": {"text": text},
            }
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, headers=self.headers)
                response.raise_for_status()
                result = response.json()
                logger.info(f"✅ MESSAGE SENT to {number}: {text}")
                return result
        except Exception as e:
            # Fallback to simulation if API fails
            logger.warning(
                f"⚠️ API failed, simulating message to {number}: {text} | Error: {str(e)}"
            )
            return {"status": "simulated", "message": text, "error": str(e)}

    async def add_tags(self, number: str, tags: List[str]):
        # Try to send real tags first, fall back to simulation
        try:
            url = f"{self.base_url}/contact/updateTags/{self.instance}"
            payload = {"number": number, "tags": tags}
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, headers=self.headers)
                response.raise_for_status()
                result = response.json()
                logger.info(f"✅ TAGS ADDED to {number}: {tags}")
                return result
        except Exception as e:
            # Fallback to simulation if API fails
            logger.warning(
                f"⚠️ Tags API failed, simulating for {number}: {tags} | Error: {str(e)}"
            )
            return {"status": "simulated", "tags": tags, "error": str(e)}


evolution_service = EvolutionService()
