from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    if not hashed_password:
        return False
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(subject: str | int, expires_delta: int = 60*60*24) -> str:
    """Create a JWT access token.

    expires_delta: seconds (default 1 day)
    """
    expire = datetime.utcnow() + timedelta(seconds=expires_delta)
    to_encode = {"sub": str(subject), "exp": expire}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt
