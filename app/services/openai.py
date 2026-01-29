from app.config import settings

class OpenAIService:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY

    async def analyze_text(self, text: str):
        # Placeholder for OpenAI text analysis
        pass

openai_service = OpenAIService()
