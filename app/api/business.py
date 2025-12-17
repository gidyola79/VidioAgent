from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Annotated
from app.db.base import get_db
from app.db.models import Business
from app.services.storage import save_voice_sample, save_avatar, get_public_url
from pydantic import BaseModel
import re

router = APIRouter()

class BusinessResponse(BaseModel):
    id: int
    name: str
    whatsapp_number: str
    owner_name: str
    business_type: str
    message: str

def validate_whatsapp_number(number: str) -> str:
    """Validate and format WhatsApp number"""
    # Remove all non-digit characters
    cleaned = re.sub(r'\D', '', number)
    
    # Ensure it starts with country code
    if not cleaned.startswith('+'):
        if len(cleaned) == 10:  # Nigerian number without country code
            cleaned = f"+234{cleaned}"
        elif len(cleaned) == 11 and cleaned.startswith('0'):
            cleaned = f"+234{cleaned[1:]}"
        else:
            cleaned = f"+{cleaned}"
    
    return cleaned

@router.post("/register", response_model=BusinessResponse)
async def register_business(
    name: Annotated[str, Form()],
    whatsapp_number: Annotated[str, Form()],
    owner_name: Annotated[str, Form()],
    business_type: Annotated[str, Form()],
    voice_sample: UploadFile = File(...),
    avatar_image: UploadFile = File(...),
    response_style: Annotated[str, Form()] = "professional",
    password: Annotated[str, Form()] = "",
    db: Session = Depends(get_db)
):
    """
    Register a new business for AI video responses.
    
    - **name**: Business name
    - **whatsapp_number**: WhatsApp Business number
    - **owner_name**: Owner's name
    - **business_type**: Type of business (e.g., Bakery, Salon)
    - **voice_sample**: Audio file of owner's voice (for ElevenLabs)
    - **avatar_image**: Photo of owner (for video generation)
    - **response_style**: AI response style (professional, casual, friendly)
    """
    
    # Validate WhatsApp number format
    try:
        formatted_number = validate_whatsapp_number(whatsapp_number)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid WhatsApp number format: {str(e)}")
    
    # Check if business already registered
    existing = db.query(Business).filter(
        Business.whatsapp_number == formatted_number
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Business with WhatsApp number {formatted_number} already registered"
        )
    
    # Validate file types
    if not voice_sample.content_type.startswith('audio/'):
        raise HTTPException(status_code=400, detail="Voice sample must be an audio file")
    
    if not avatar_image.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Avatar must be an image file")
    
    # Validate password: require a strong password (min 8 chars)
    if not password or len(password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")

    # Save uploaded files
    try:
        voice_path = await save_voice_sample(voice_sample)
        avatar_path = await save_avatar(avatar_image)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save files: {str(e)}")
    
    # Create business record
    business = Business(
        name=name,
        whatsapp_number=formatted_number,
        owner_name=owner_name,
        business_type=business_type,
        voice_sample_url=voice_path,
        avatar_image_url=avatar_path,
        response_style=response_style,
        is_active=True
    )

    # If a password was provided, hash and store it
    try:
        from app.core.security import hash_password
        if password:
            business.password_hash = hash_password(password)
    except Exception:
        # If hashing fails, continue but warn in logs
        print("Warning: password hashing failed; password not saved")
    
    db.add(business)
    db.commit()
    db.refresh(business)
    
    return BusinessResponse(
        id=business.id,
        name=business.name,
        whatsapp_number=business.whatsapp_number,
        owner_name=business.owner_name,
        business_type=business.business_type,
        message=f"Business '{name}' registered successfully! You can now receive AI video responses on {formatted_number}"
    )

@router.get("/businesses/{business_id}")
async def get_business(business_id: int, db: Session = Depends(get_db)):
    """Get business details by ID"""
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    
    return {
        "id": business.id,
        "name": business.name,
        "whatsapp_number": business.whatsapp_number,
        "owner_name": business.owner_name,
        "business_type": business.business_type,
        "is_active": business.is_active,
        "created_at": business.created_at
    }

@router.get("/businesses")
async def list_businesses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """List all registered businesses"""
    businesses = db.query(Business).offset(skip).limit(limit).all()
    return [
        {
            "id": b.id,
            "name": b.name,
            "whatsapp_number": b.whatsapp_number,
            "business_type": b.business_type,
            "is_active": b.is_active
        }
        for b in businesses
    ]
