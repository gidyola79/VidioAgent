from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Use SQLite for development if DATABASE_URL not set
if settings.DATABASE_URL:
    engine = create_engine(settings.DATABASE_URL)
else:
    # SQLite fallback for local development
    engine = create_engine("sqlite:///./vidioagent.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
