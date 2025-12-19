from fastapi import APIRouter, Form, HTTPException, Request, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.base import get_db
from app.db.models import Business, Customer, Conversation
from app.services.twilio_service import send_whatsapp_message

router = APIRouter()

def trigger_task(...):
    from app.celery_app import generate_and_send_video
    generate_and_send_video.delay(...)
    
def get_or_create_customer(phone_number: str, business_id: int, db: Session) -> Customer:
    """Get existing customer or create new one"""
    customer = db.query(Customer).filter(
        Customer.phone_number == phone_number,
        Customer.business_id == business_id
    ).first()
    
    if not customer:
        customer = Customer(
            phone_number=phone_number,
            business_id=business_id
        )
        db.add(customer)
        db.commit()
        db.refresh(customer)
    
    return customer

@router.post("/webhook")
async def whatsapp_webhook(
    From: Annotated[str, Form()],
    To: Annotated[str, Form()],
    Body: Annotated[str, Form()],
    db: Session = Depends(get_db)
):
    """
    Handle incoming WhatsApp messages from Twilio.
    
    Multi-tenant flow:
    1. Look up which business owns the 'To' WhatsApp number
    2. Create/get customer record
    3. Create conversation record
    4. Send immediate acknowledgment
    5. Trigger async video generation
    """
    print(f"Received message from {From} to {To}: {Body}")
    
    # Extract WhatsApp number from 'To' field
    # Twilio sends in format: whatsapp:+1234567890
    business_number = To.replace("whatsapp:", "")
    
    # 1. Find the business
    business = db.query(Business).filter(
        Business.whatsapp_number == business_number
    ).first()
    
    if not business:
        print(f"No business found for WhatsApp number: {business_number}")
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>This business is not registered with VidioAgent.</Message>
</Response>'''
    
    if not business.is_active:
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>This business account is currently inactive.</Message>
</Response>'''
    
    # 2. Get or create customer
    customer_phone = From.replace("whatsapp:", "")
    customer = get_or_create_customer(customer_phone, business.id, db)
    
    # 3. Create conversation record
    conversation = Conversation(
        business_id=business.id,
        customer_id=customer.id,
        message_from_customer=Body,
        status="pending"
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    
    # 4. Send immediate acknowledgment
    try:
        send_whatsapp_message(
            From,
            f"Hi! Thanks for messaging {business.name}. I'm preparing a personalized video response for you... 🎥"
        )
    except Exception as e:
        print(f"Failed to send acknowledgment: {e}")
    
    # 5. Trigger async video generation
    generate_and_send_video.delay(
        conversation_id=conversation.id,
        business_id=business.id,
        customer_phone=From,
        message_text=Body
    )
    
    # Return empty response (we already sent acknowledgment via Twilio API)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<Response></Response>'''
