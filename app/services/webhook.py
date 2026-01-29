import httpx
import json
import uuid
from datetime import datetime, timezone
from app.config import settings
from typing import Dict, Any, List, Tuple
import logging

logger = logging.getLogger(__name__)


class WebhookService:
    def __init__(self):
        self.prod_webhook_url = settings.EXTERNAL_WEBHOOK_URL_PROD
        self.test_webhook_url = settings.EXTERNAL_WEBHOOK_URL_TEST
        self.timeout = 30

    async def send_lead_data(self, lead_data: Dict[str, Any]) -> bool:
        """
        Send lead data to both production and test webhooks with UUID for tracking

        Args:
            lead_data: Dictionary containing lead information

        Returns:
            bool: True if successful to at least one webhook, False otherwise
        """
        webhooks = []
        if self.prod_webhook_url:
            webhooks.append(("production", self.prod_webhook_url))
        if self.test_webhook_url:
            webhooks.append(("test", self.test_webhook_url))

        if not webhooks:
            logger.warning("No webhook URLs configured")
            return False

        # Generate unique UUID for this submission
        submission_id = str(uuid.uuid4())

        # Prepare payload with metadata
        payload = {
            "uuid": submission_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source": "NOA_BOT",
            "instance": settings.EVOLUTION_INSTANCE,
            "data": lead_data,
        }

        success_count = 0

        for webhook_type, webhook_url in webhooks:
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(
                        webhook_url,
                        json=payload,
                        headers={
                            "Content-Type": "application/json",
                            "User-Agent": "NOA-Bot/1.0",
                        },
                    )

                    if response.status_code in [200, 201, 202]:
                        logger.info(
                            f"Successfully sent lead data {submission_id} to {webhook_type} webhook"
                        )
                        success_count += 1
                    else:
                        logger.error(
                            f"Failed to send lead data to {webhook_type}. Status: {response.status_code}, Response: {response.text}"
                        )

            except httpx.TimeoutException:
                logger.error(f"Timeout when sending data to {webhook_type} webhook")
            except Exception as e:
                logger.error(
                    f"Error sending lead data to {webhook_type} webhook: {str(e)}"
                )

        return success_count > 0

    async def send_conversation_log(
        self, phone: str, message: str, response: str, state: str
    ) -> bool:
        """
        Send conversation log to both production and test webhooks

        Args:
            phone: User phone number
            message: User message
            response: Bot response
            state: Current conversation state

        Returns:
            bool: True if successful to at least one webhook, False otherwise
        """
        webhooks = []
        if self.prod_webhook_url:
            webhooks.append(("production", self.prod_webhook_url))
        if self.test_webhook_url:
            webhooks.append(("test", self.test_webhook_url))

        if not webhooks:
            return False

        log_data = {
            "uuid": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "type": "conversation_log",
            "phone": phone,
            "user_message": message,
            "bot_response": response,
            "state": state,
            "instance": settings.EVOLUTION_INSTANCE,
        }

        success_count = 0

        for webhook_type, webhook_url in webhooks:
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    resp = await client.post(
                        webhook_url,
                        json=log_data,
                        headers={
                            "Content-Type": "application/json",
                            "User-Agent": "NOA-Bot/1.0",
                        },
                    )

                    if resp.status_code in [200, 201, 202]:
                        success_count += 1
                        logger.info(
                            f"Successfully sent conversation log to {webhook_type} webhook"
                        )
                    else:
                        logger.error(
                            f"Failed to send conversation log to {webhook_type}. Status: {resp.status_code}"
                        )

            except Exception as e:
                logger.error(
                    f"Error sending conversation log to {webhook_type} webhook: {str(e)}"
                )

        return success_count > 0


webhook_service = WebhookService()
