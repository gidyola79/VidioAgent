from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.get("/ready")
async def ready():
    # Basic readiness: check minimal required settings
    ok = True
    missing = []
    if not settings.SECRET_KEY or settings.SECRET_KEY in ("change-me", "development_secret"):
        missing.append("SECRET_KEY")
        ok = False
    return {"ready": ok, "missing": missing}
