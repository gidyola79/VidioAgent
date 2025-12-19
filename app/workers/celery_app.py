from celery import Celery
from app.core.config import settings

celery_app = Celery("vidioagent", broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

@celery_app.task(bind=True, max_retries=3)
def generate_and_send_video(
    self,
    conversation_id: int,
    business_id: int,
    customer_phone: str,
    message_text: str
):

# SSL support (important if using Upstash / Railway Redis TLS)
if settings.CELERY_BROKER_URL.startswith("rediss://"):
    celery_app.conf.broker_use_ssl = {"ssl_cert_reqs": "required"}
    celery_app.conf.redis_backend_use_ssl = {"ssl_cert_reqs": "required"}

    
    """
    Generate AI video response and send to customer via WhatsApp.
    
    This task:
    1. Gets business profile (voice, avatar)
    2. Generates AI text response
    3. Generates voice audio from text
    4. Generates lip-sync video
    5. Sends video to customer
    6. Updates conversation status
    """
    from app.db.base import SessionLocal
    from app.db.models import Business, Conversation
    from app.agent.graph import app_graph
    from langchain_core.messages import HumanMessage
    from app.services.voice import generate_voice_from_text
    from app.services.video import generate_talking_head_video
    from app.services.storage import save_audio, get_public_url
    from app.services.twilio_service import send_whatsapp_media, send_whatsapp_message
    import asyncio
    
    db = SessionLocal()
    
    try:
        # 1. Get business and conversation
        business = db.query(Business).filter(Business.id == business_id).first()
        conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        
        if not business or not conversation:
            raise Exception("Business or conversation not found")
        
        conversation.status = "processing"
        db.commit()
        
        # 2. Generate AI response text
        initial_state = {"messages": [HumanMessage(content=message_text)]}
        result = app_graph.invoke(initial_state)
        ai_response = result["messages"][-1].content
        
        conversation.ai_response_text = ai_response
        db.commit()
        
        # 3. Generate voice audio
        # Note: For now using default voice, in production would use cloned voice
        audio_bytes = asyncio.run(generate_voice_from_text(ai_response))
        audio_path = asyncio.run(save_audio(audio_bytes))
        audio_url = get_public_url(audio_path)
        
        # Make audio URL absolute
        # In production, this would be your deployed backend URL
        base_url = "http://localhost:8000"  # TODO: Use settings.BASE_URL
        if not audio_url.startswith("http"):
            audio_url = f"{base_url}{audio_url}"
        
        # 4. Get avatar URL
        avatar_url = get_public_url(business.avatar_image_url)
        if not avatar_url.startswith("http"):
            avatar_url = f"{base_url}{avatar_url}"
        
        # 5. Generate video
        video_url = asyncio.run(generate_talking_head_video(audio_url, avatar_url))
        
        conversation.video_url = video_url
        db.commit()
        
        # 6. Send video to customer
        send_whatsapp_media(
            customer_phone,
            video_url,
            caption=f"Hi! Here's my response from {business.name}"
        )
        
        conversation.status = "sent"
        conversation.sent_at = asyncio.run(asyncio.coroutine(lambda: __import__('datetime').datetime.utcnow())())
        db.commit()
        
        return {
            "status": "success",
            "conversation_id": conversation_id,
            "video_url": video_url
        }
        
    except Exception as e:
        # Update conversation status to failed
        if conversation:
            conversation.status = "failed"
            conversation.error_message = str(e)
            db.commit()
        
        # Retry with exponential backoff
        raise self.retry(exc=e, countdown=60 * (2 ** self.request.retries))
        
    finally:
        db.close()
