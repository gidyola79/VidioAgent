# VidioAgent

VidioAgent is an AI-powered service that receives WhatsApp messages for registered businesses, generates a personalized spoken response and lip-synced video, and sends it back to the customer.

This repository contains a FastAPI backend, Celery worker, and a Next.js frontend.

## Quick start (development)

Prerequisites:
- Python 3.11 (recommended)
- Node.js & npm
- Docker (optional, recommended for Redis)

1. Copy `.env.example` to `.env` and fill in the required API keys and settings.

Password policy: business owner accounts require a password with a minimum of 8 characters. Use a mix of uppercase, lowercase, numbers, and symbols for stronger protection.

2. (Optional) Start Redis with Docker for Celery:
```powershell
docker run -d -p 6379:6379 --name redis redis:7
```

3. Create and activate a Python virtual environment (use Python 3.11):
```powershell
cd C:\Users\HP\PROJECTS
py -3.11 -m venv .venv
& .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

4. Initialize the database (dev - SQLite) or run migrations:
```powershell
# Option A: quick create tables (dev)
python -c "from app.db.base import Base, engine; Base.metadata.create_all(bind=engine)"

# Option B: use alembic migrations if you prefer
alembic upgrade head
```

5. Start the backend API:
```powershell
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Alternatively, you can start the backend in a separate PowerShell window from the repo root:
```powershell
cd C:\Users\HP\PROJECTS
& .\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

6. Start a Celery worker (in a separate terminal with the venv activated):
```powershell
# If celery is on PATH
celery -A app.workers.celery_app.celery_app worker --loglevel=info

# Or via python module
python -m celery -A app.workers.celery_app.celery_app worker --loglevel=info
```

7. Start the frontend (in the `frontend/` folder):
```powershell
cd frontend
npm install
npm run dev
```

Tip: Start the frontend in its own terminal so you can watch the Next.js logs while developing.

8. For Twilio webhooks during local dev, use `ngrok` to expose your local backend and set the Twilio webhook URL to `https://<ngrok-id>.ngrok.io/whatsapp/webhook`.

## Important environment variables
See `.env.example` for a full list. Minimum keys for E2E:
- `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_WHATSAPP_NUMBER`
- `ELEVENLABS_API_KEY`
- `REPLICATE_API_TOKEN`
- `GROQ_API_KEY` (or other LLM provider key)
- `CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND` (Redis recommended)

## Production notes
- Use managed Postgres for `DATABASE_URL`.
- Use S3 or another cloud object store for media (replace `app/services/storage.py`).
- Deploy Celery workers on a worker pool (separate processes/hosts).
- Replace local `BASE_URL` with your production backend URL so media links are absolute.
- Ensure Twilio WhatsApp sender is approved for production use (Twilio sandbox vs Business API differences).

## Next recommended changes
- Use Python 3.11 to avoid binary wheel compatibility issues (e.g., `pydantic-core`).
- Clone voice sample during registration and store the ElevenLabs voice ID so generated audio uses the owner's voice.
- Add automated tests and a GitHub Actions workflow for CI.

## Contact / Support
If you want, I can:
- Recreate the venv here with Python 3.11 and reinstall deps.
- Wire voice cloning into business registration.
- Add a `README` section for deploying to Render / Vercel / Fly.

## Docker & Deployment

You can run a local development stack using Docker Compose (includes Redis, backend and frontend services):

```powershell
docker-compose up --build
```

Deployment checklist:

- Ensure `.env` is populated with real secrets (do **not** use `change-me` as `SECRET_KEY`).
- Run Alembic migrations before starting the service in production: `alembic upgrade head` (a migration to add `password_hash` is included).
- Use managed services for Redis and a production database (Postgres) in production environments.
- Configure HTTPS at the edge (load balancer) and set `BASE_URL` to your production backend URL.
- Rotate API keys and store them in a secure vault rather than checked-in `.env` for production.
- Run multiple Celery worker processes (and autoscale) for background tasks.
- Consider using a process manager (systemd / supervisord) or container orchestrator (Kubernetes) for reliability.

