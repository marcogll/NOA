from fastapi import APIRouter, Request, BackgroundTasks, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.services.evolution import evolution_service
from app.services.openai import openai_service
from app.services.rag import rag_service
from app.services.webhook import webhook_service
from app.flows.states import ConversationManager, NOAState
from app.db.async_session import get_async_db, AsyncSessionLocal
from app.db.models import Lead
from app.schemas.webhooks import (
    EvolutionWebhookPayload,
    PhoneValidator,
    WebhookDataProcessor,
)
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


async def handle_conversation(
    number: str,
    text: str,
    background_tasks: BackgroundTasks = None,
    db: AsyncSession = None,
):
    manager = ConversationManager(number)
    state = manager.get_state()

    try:
        # Get or create lead using async
        result = await db.execute(select(Lead).where(Lead.phone == number))
        lead = result.scalar_one_or_none()

        if not lead:
            lead = Lead(phone=number)
            db.add(lead)
            await db.commit()
            await db.refresh(lead)

        if state == NOAState.INIT:
            await evolution_service.send_message(
                number,
                "Bienvenido a Noire Collective. Soy NOA 👋 ¿Podría darme su nombre?",
            )
            manager.transition_to(NOAState.ASK_NAME)
            await evolution_service.add_tags(number, ["NEW_LEAD"])

        elif state == NOAState.ASK_NAME:
            lead.name = text
            await db.commit()
            await evolution_service.send_message(
                number, f"Mucho gusto, {text} 😊 ¿Cuál es su industria de negocio?"
            )
            manager.transition_to(NOAState.ASK_INDUSTRY)

        elif state == NOAState.ASK_INDUSTRY:
            lead.industry = text
            await db.commit()
            await evolution_service.send_message(
                number,
                "Entendido 📱 ¿Tienes perfiles en redes sociales para tu negocio? Por favor comparte los enlaces o usuarios.",
            )
            manager.transition_to(NOAState.ASK_SOCIAL_MEDIA)

        elif state == NOAState.ASK_SOCIAL_MEDIA:
            lead.social_media = text
            await db.commit()
            await evolution_service.send_message(
                number,
                "Gracias 📝 ¿Cuál es el principal problema u objetivo que quieres que te ayudemos con?",
            )
            manager.transition_to(NOAState.ASK_PROBLEM)

        elif state == NOAState.ASK_PROBLEM:
            lead.problem = text
            await db.commit()
            await evolution_service.send_message(
                number, "Gracias por la información 🙏 Estoy analizando tu solicitud..."
            )
            manager.transition_to(NOAState.ANALYZE)

            # Perform OpenAI analysis
            analysis = await openai_service.analyze_text(text)
            lead.sentiment = analysis.get("sentiment", "neutral")
            lead.intent = analysis.get("intent", "unknown")
            lead.lead_score = analysis.get("score", 50)
            await db.commit()

            # Move to recommend state based on analysis
            manager.transition_to(NOAState.RECOMMEND)

            # Get personalized recommendation using RAG
            lead_info = {
                "name": lead.name,
                "industry": lead.industry,
                "problem": lead.problem,
                "sentiment": lead.sentiment,
                "lead_score": lead.lead_score,
            }

            recommendation = await rag_service.search_context(text, lead_info)

            # Save recommendation
            lead.recommended_service = recommendation.get("name", "Plan Estándar")
            await db.commit()

            # Send personalized recommendation
            rec_type = recommendation.get("type", "plan")
            emoji = "🎯" if rec_type == "plan" else "🛠️"

            response_message = f"Basado en tu análisis {emoji}, te recomiendo nuestro {recommendation['name']}: {recommendation['description']} por {recommendation['price']}. ¿Te gustaría que un agente te contacte para más detalles?"

            await evolution_service.send_message(number, response_message)

            # Send lead data to external webhook
            lead_data = {
                "phone": lead.phone,
                "name": lead.name,
                "industry": lead.industry,
                "social_media": lead.social_media,
                "problem": lead.problem,
                "sentiment": lead.sentiment,
                "intent": lead.intent,
                "lead_score": lead.lead_score,
                "recommended_service": lead.recommended_service,
                "state": "CLOSED",
            }

            # Send data asynchronously if background_tasks is available
            if background_tasks:
                background_tasks.add_task(webhook_service.send_lead_data, lead_data)
            else:
                # Send directly if no background_tasks
                await webhook_service.send_lead_data(lead_data)

            manager.transition_to(NOAState.CLOSED)

    except Exception as e:
        logger.error(f"Error handling conversation for {number}: {str(e)}")
        # Try to send error message
        try:
            await evolution_service.send_message(
                number,
                "Lo siento, tuve un problema. Por favor intenta de nuevo más tarde.",
            )
        except:
            pass
    finally:
        if db:
            await db.close()


@router.post("/webhook")
async def evolution_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_async_db),
):
    try:
        # Parse and validate JSON
        data = await request.json()

        # Validate webhook payload structure
        try:
            webhook_payload = EvolutionWebhookPayload(**data)
        except Exception as validation_error:
            logger.warning(f"Webhook validation failed: {validation_error}")
            raise HTTPException(status_code=400, detail="Invalid webhook payload")

        # Extract message data
        message_data = webhook_payload.data
        key_data = message_data.get("key", {})

        # Skip messages from ourselves
        if key_data.get("fromMe", False):
            return {"status": "ignored_from_me"}

        # Extract and validate phone number
        try:
            phone = PhoneValidator.extract_phone(key_data.get("remoteJid", ""))
        except ValueError as phone_error:
            logger.warning(f"Phone validation failed: {phone_error}")
            raise HTTPException(status_code=400, detail="Invalid phone number")

        # Extract message text
        text = WebhookDataProcessor.extract_text(message_data)
        if not text:
            return {"status": "no_text"}

        # Process conversation asynchronously
        # Create a new DB session for the background task
        async def process_with_db():
            async with AsyncSessionLocal() as db_session:
                await handle_conversation(phone, text, background_tasks, db_session)

        background_tasks.add_task(process_with_db)

        return {"status": "accepted", "phone": phone}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Webhook processing error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
