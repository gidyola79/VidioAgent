from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.db.base import get_db
from app.db.models import Business
from sqlalchemy.orm import Session
from app.core.security import verify_password, create_access_token


router = APIRouter()

class LoginRequest(BaseModel):
    phone: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


def normalize_phone(p: str) -> str:
    if p.startswith("whatsapp:"):
        p = p.replace("whatsapp:", "")
    # Keep as provided if starts with +, otherwise try to add +
    if not p.startswith("+"):
        cleaned = ''.join([c for c in p if c.isdigit()])
        if cleaned:
            p = f"+{cleaned}"
    return p


@router.post("/login", response_model=LoginResponse)
async def login(req: LoginRequest, db: Session = Depends(get_db)):
    # normalize and find business by whatsapp number
    phone = normalize_phone(req.phone)

    business = db.query(Business).filter(Business.whatsapp_number == phone).first()
    if not business:
        # try matching without plus or with whatsapp: prefix
        business = db.query(Business).filter(Business.whatsapp_number == f"whatsapp:{phone}").first()

    if not business:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(req.password, business.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token(subject=business.id)
    return LoginResponse(access_token=token)
