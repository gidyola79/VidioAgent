"""Twilio WhatsApp messaging service"""
from twilio.rest import Client
from app.core.config import settings

def get_twilio_client() -> Client:
    """Get configured Twilio client"""
    if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
        raise ValueError("Twilio credentials not set in environment")
    
    return Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

def send_whatsapp_message(to_number: str, message: str) -> str:
    """
    Send a text message via WhatsApp.
    
    Args:
        to_number: Recipient WhatsApp number (format: whatsapp:+1234567890)
        message: Message text to send
        
    Returns:
        Message SID
    """
    client = get_twilio_client()
    
    if not to_number.startswith("whatsapp:"):
        to_number = f"whatsapp:{to_number}"
    
    from_number = f"whatsapp:{settings.TWILIO_WHATSAPP_NUMBER}"
    
    message = client.messages.create(
        body=message,
        from_=from_number,
        to=to_number
    )
    
    return message.sid

def send_whatsapp_media(to_number: str, media_url: str, caption: str = "") -> str:
    """
    Send media (image/video) via WhatsApp.
    
    Args:
        to_number: Recipient WhatsApp number
        media_url: Public URL to the media file
        caption: Optional caption for the media
        
    Returns:
        Message SID
    """
    client = get_twilio_client()
    
    if not to_number.startswith("whatsapp:"):
        to_number = f"whatsapp:{to_number}"
    
    from_number = f"whatsapp:{settings.TWILIO_WHATSAPP_NUMBER}"
    
    message = client.messages.create(
        body=caption,
        from_=from_number,
        to=to_number,
        media_url=[media_url]
    )
    
    return message.sid
