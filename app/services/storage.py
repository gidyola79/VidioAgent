"""File storage service for voice samples, avatars, and generated videos"""
import os
import uuid
from pathlib import Path
from fastapi import UploadFile
from app.core.config import settings

# Storage directory
STORAGE_DIR = Path("./storage")
VOICE_SAMPLES_DIR = STORAGE_DIR / "voice_samples"
AVATARS_DIR = STORAGE_DIR / "avatars"
VIDEOS_DIR = STORAGE_DIR / "videos"
AUDIO_DIR = STORAGE_DIR / "audio"

# Create directories if they don't exist
for directory in [VOICE_SAMPLES_DIR, AVATARS_DIR, VIDEOS_DIR, AUDIO_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

async def save_voice_sample(file: UploadFile) -> str:
    """Save voice sample and return file path"""
    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = VOICE_SAMPLES_DIR / unique_filename
    
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
    
    return str(file_path)

async def save_avatar(file: UploadFile) -> str:
    """Save avatar image and return file path"""
    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = AVATARS_DIR / unique_filename
    
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
    
    return str(file_path)

async def save_audio(audio_bytes: bytes, extension: str = ".mp3") -> str:
    """Save generated audio and return file path"""
    unique_filename = f"{uuid.uuid4()}{extension}"
    file_path = AUDIO_DIR / unique_filename
    
    with open(file_path, "wb") as f:
        f.write(audio_bytes)
    
    return str(file_path)

async def save_video(video_url: str) -> str:
    """Download and save video from URL, return local path"""
    import httpx
    
    unique_filename = f"{uuid.uuid4()}.mp4"
    file_path = VIDEOS_DIR / unique_filename
    
    async with httpx.AsyncClient() as client:
        response = await client.get(video_url)
        with open(file_path, "wb") as f:
            f.write(response.content)
    
    return str(file_path)

def get_public_url(file_path: str) -> str:
    """Convert file path to public URL (for now, just return the path)"""
    # In production, this would return a CDN URL or S3 URL
    # For now, we'll serve files statically from the storage directory
    return f"/storage/{Path(file_path).relative_to(STORAGE_DIR)}"
