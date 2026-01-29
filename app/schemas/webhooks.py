from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
import re


class EvolutionWebhookPayload(BaseModel):
    event: str = Field(..., description="Event type")
    data: Dict[str, Any] = Field(..., description="Message data")

    @validator("event")
    def validate_event(cls, v):
        if v != "messages.upsert":
            raise ValueError("Invalid event type")
        return v


class MessageKey(BaseModel):
    remoteJid: str = Field(..., description="Remote JID")
    fromMe: bool = Field(..., description="From me flag")
    id: str = Field(..., description="Message ID")

    @validator("remoteJid")
    def validate_remote_jid(cls, v):
        if not v or "@" not in v:
            raise ValueError("Invalid remote JID")
        return v


class MessageContent(BaseModel):
    conversation: Optional[str] = Field(None, description="Conversation text")
    extendedTextMessage: Optional[Dict[str, Any]] = Field(
        None, description="Extended text message"
    )

    @validator("conversation", "extendedTextMessage", pre=True)
    def validate_message_content(cls, v):
        if v is None:
            return v
        if isinstance(v, str) and len(v.strip()) == 0:
            return None
        return v


class EvolutionMessageData(BaseModel):
    key: MessageKey = Field(..., description="Message key")
    message: MessageContent = Field(..., description="Message content")

    class Config:
        extra = "forbid"  # Disallow extra fields


class PhoneValidator:
    @staticmethod
    def extract_phone(remote_jid: str) -> str:
        """Extract phone number from JID"""
        if not remote_jid:
            raise ValueError("Empty remote JID")

        # Extract phone part before @
        phone = remote_jid.split("@")[0]

        # Basic phone validation
        if not re.match(r"^\d+$", phone):
            raise ValueError(f"Invalid phone format: {phone}")

        return phone


class WebhookDataProcessor:
    @staticmethod
    def extract_text(message_data: Dict[str, Any]) -> Optional[str]:
        """Extract text message from webhook data"""
        try:
            message_content = message_data.get("message", {})
            text = message_content.get("conversation")

            if not text:
                extended_message = message_content.get("extendedTextMessage", {})
                text = extended_message.get("text")

            return text.strip() if text and text.strip() else None
        except Exception:
            return None
