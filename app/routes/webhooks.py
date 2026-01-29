from fastapi import APIRouter, Request, BackgroundTasks
from app.services.evolution import evolution_service
from app.flows.states import ConversationManager, NOAState
from app.db.session import SessionLocal
from app.db.models import Lead
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

async def handle_conversation(number: str, text: str):
    manager = ConversationManager(number)
    state = manager.get_state()

    db = SessionLocal()
    try:
        # Get or create lead
        lead = db.query(Lead).filter(Lead.phone == number).first()
        if not lead:
            lead = Lead(phone=number)
            db.add(lead)
            db.commit()
            db.refresh(lead)

        if state == NOAState.INIT:
            await evolution_service.send_message(number, "Welcome to Noire Collective. I am NOA. May I have your name?")
            manager.transition_to(NOAState.ASK_NAME)
            await evolution_service.add_tags(number, ["NEW_LEAD"])

        elif state == NOAState.ASK_NAME:
            lead.name = text
            db.commit()
            await evolution_service.send_message(number, f"Nice to meet you, {text}. What is your business industry?")
            manager.transition_to(NOAState.ASK_INDUSTRY)

        elif state == NOAState.ASK_INDUSTRY:
            lead.industry = text
            db.commit()
            await evolution_service.send_message(number, "Got it. Do you have social media profiles for your business? Please share links or handles.")
            manager.transition_to(NOAState.ASK_SOCIAL_MEDIA)

        elif state == NOAState.ASK_SOCIAL_MEDIA:
            lead.social_media = text
            db.commit()
            await evolution_service.send_message(number, "Thank you. What is the main problem or goal you want us to help you with?")
            manager.transition_to(NOAState.ASK_PROBLEM)

        elif state == NOAState.ASK_PROBLEM:
            lead.problem = text
            db.commit()
            await evolution_service.send_message(number, "Thank you for the information. I am analyzing your request...")
            manager.transition_to(NOAState.ANALYZE)
            # OpenAI analysis logic would go here in Phase 2

    finally:
        db.close()

@router.post("/webhook")
async def evolution_webhook(request: Request, background_tasks: BackgroundTasks):
    try:
        data = await request.json()
    except Exception:
        return {"status": "invalid_json"}

    event = data.get("event")
    if event != "messages.upsert":
        return {"status": "ignored_event"}

    message_data = data.get("data", {})
    key = message_data.get("key", {})
    if key.get("fromMe"):
        return {"status": "ignored_from_me"}

    remote_jid = key.get("remoteJid")
    if not remote_jid:
        return {"status": "no_remote_jid"}

    number = remote_jid.split("@")[0]

    message_content = message_data.get("message", {})
    text = message_content.get("conversation") or \
           message_content.get("extendedTextMessage", {}).get("text")

    if not text:
        return {"status": "no_text"}

    background_tasks.add_task(handle_conversation, number, text)

    return {"status": "accepted"}
