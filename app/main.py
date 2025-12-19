from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api import whatsapp, web, business, auth
from app.core.config import settings
import os

app = FastAPI(title="VidioAgent API", version="0.1.0")

# Mount storage directory for serving uploaded files
if os.path.exists("./storage"):
    app.mount("/storage", StaticFiles(directory="storage"), name="storage")

# Configure CORS for frontend access using BASE_URL if provided
allowed = [settings.BASE_URL] if settings.BASE_URL else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#@app.middleware("http")
#async def add_security_headers(request: Request, call_next):
    #resp = await call_next(request)
    # Basic security headers
    #resp.headers.setdefault("X-Frame-Options", "DENY")
    #resp.headers.setdefault("X-Content-Type-Options", "nosniff")
    #resp.headers.setdefault("Referrer-Policy", "no-referrer")
    #resp.headers.setdefault("Strict-Transport-Security", "max-age=63072000; includeSubDomains; preload")
    #resp.headers.setdefault("Permissions-Policy", "geolocation=(), microphone=()")
    #return resp


@app.on_event("startup")
async def startup_checks():
    # Warn when essential env vars are missing or left as defaults
    if settings.SECRET_KEY in (None, "change-me", "development_secret"):
        print("WARNING: SECRET_KEY is not set or uses the default value. Set a strong SECRET_KEY in .env before production.")
    if not settings.ELEVENLABS_API_KEY and not settings.REPLICATE_API_TOKEN and not settings.OPENAI_API_KEY and not settings.GROQ_API_KEY:
        print("INFO: No AI provider keys set. Some features may be disabled until you provide API keys.")


@app.get("/")
async def root():
    return {"message": "VidioAgent API is running"}


@app.get('/health')
async def health():
    return {"status": "ok"}


#@app.get('/ready')
#async def ready():
    # Basic readiness check: DB connectivity
   # try:
       # from app.db.base import engine
       # with engine.connect() as conn:
           # conn.execute("SELECT 1")
   # except Exception:
       # raise RuntimeError("db-unavailable")
    #return {"status": "ready"}


app.include_router(whatsapp.router, prefix="/whatsapp", tags=["whatsapp"])
app.include_router(web.router, prefix="/api", tags=["web"])
app.include_router(business.router, prefix="/api/business", tags=["business"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
from app.api import health

app.include_router(health.router, tags=["health"])


#if __name__ == "__main__":
    #import uvicorn
    #uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
