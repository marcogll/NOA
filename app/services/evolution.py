import httpx
from app.config import settings
from typing import List, Optional

class EvolutionService:
    def __init__(self):
        self.base_url = settings.EVOLUTION_API_URL
        self.api_key = settings.EVOLUTION_API_TOKEN
        self.instance = settings.EVOLUTION_INSTANCE
        self.headers = {
            "apikey": self.api_key,
            "Content-Type": "application/json"
        }

    async def send_message(self, number: str, text: str):
        url = f"{self.base_url}/message/sendText/{self.instance}"
        payload = {
            "number": number,
            "options": {
                "delay": 1200,
                "presence": "composing"
            },
            "text_message": {
                "text": text
            }
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()

    async def add_tags(self, number: str, tags: List[str]):
        url = f"{self.base_url}/contact/updateTags/{self.instance}"
        payload = {
            "number": number,
            "tags": tags
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()

evolution_service = EvolutionService()
