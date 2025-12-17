"""ElevenLabs voice generation service"""
from elevenlabs import generate, Voice, VoiceSettings, save
from app.core.config import settings
import httpx
from pathlib import Path

async def generate_voice_from_text(
    text: str,
    voice_id: str = "21m00Tcm4TlvDq8ikWAM",  # Default voice
    model: str = "eleven_multilingual_v2"
) -> bytes:
    """
    Generate audio from text using ElevenLabs.
    
    Args:
        text: Text to convert to speech
        voice_id: ElevenLabs voice ID (or custom cloned voice)
        model: Model to use for generation
        
    Returns:
        Audio bytes (MP3 format)
    """
    if not settings.ELEVENLABS_API_KEY:
        raise ValueError("ELEVENLABS_API_KEY not set in environment")
    
    try:
        audio = generate(
            text=text,
            voice=Voice(
                voice_id=voice_id,
                settings=VoiceSettings(
                    stability=0.5,
                    similarity_boost=0.75,
                    style=0.0,
                    use_speaker_boost=True
                )
            ),
            model=model,
            api_key=settings.ELEVENLABS_API_KEY
        )
        
        # Convert generator to bytes
        audio_bytes = b"".join(audio)
        return audio_bytes
        
    except Exception as e:
        raise Exception(f"ElevenLabs voice generation failed: {str(e)}")

async def clone_voice_from_sample(
    voice_sample_path: str,
    voice_name: str
) -> str:
    """
    Clone a voice from an audio sample using ElevenLabs API.
    
    Args:
        voice_sample_path: Path to the voice sample audio file
        voice_name: Name for the cloned voice
        
    Returns:
        Voice ID of the cloned voice
    """
    if not settings.ELEVENLABS_API_KEY:
        raise ValueError("ELEVENLABS_API_KEY not set in environment")
    
    url = "https://api.elevenlabs.io/v1/voices/add"
    
    headers = {
        "xi-api-key": settings.ELEVENLABS_API_KEY
    }
    
    # Read the voice sample file
    with open(voice_sample_path, "rb") as f:
        files = {
            "files": (Path(voice_sample_path).name, f, "audio/mpeg")
        }
        data = {
            "name": voice_name,
            "description": f"Cloned voice for {voice_name}"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, files=files, data=data)
            
            if response.status_code != 200:
                raise Exception(f"Voice cloning failed: {response.text}")
            
            result = response.json()
            return result["voice_id"]

async def get_available_voices() -> list:
    """Get list of available voices from ElevenLabs"""
    if not settings.ELEVENLABS_API_KEY:
        raise ValueError("ELEVENLABS_API_KEY not set in environment")
    
    url = "https://api.elevenlabs.io/v1/voices"
    headers = {"xi-api-key": settings.ELEVENLABS_API_KEY}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()["voices"]
        else:
            raise Exception(f"Failed to get voices: {response.text}")
