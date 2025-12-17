"""Replicate video generation service for lip-sync videos"""
import replicate
from app.core.config import settings
import httpx
from pathlib import Path

async def generate_talking_head_video(
    audio_url: str,
    image_url: str,
    output_path: str = None
) -> str:
    """
    Generate a lip-synced talking head video using Replicate's SadTalker model.
    
    Args:
        audio_url: URL to the audio file (voice)
        image_url: URL to the avatar image
        output_path: Optional local path to save the video
        
    Returns:
        URL to the generated video
    """
    if not settings.REPLICATE_API_TOKEN:
        raise ValueError("REPLICATE_API_TOKEN not set in environment")
    
    try:
        # Initialize Replicate client
        client = replicate.Client(api_token=settings.REPLICATE_API_TOKEN)
        
        # Run SadTalker model
        output = client.run(
            "cjwbw/sadtalker:3aa3dac9353cc4d6bd62a35e0f93b766889e0be6f882ed4adf43f3e",
            input={
                "source_image": image_url,
                "driven_audio": audio_url,
                "preprocess": "full",
                "still_mode": False,
                "use_enhancer": True,
                "batch_size": 1
            }
        )
        
        # Output is a URL to the generated video
        video_url = str(output)
        
        # Optionally download the video locally
        if output_path:
            async with httpx.AsyncClient() as http_client:
                response = await http_client.get(video_url)
                with open(output_path, "wb") as f:
                    f.write(response.content)
        
        return video_url
        
    except Exception as e:
        raise Exception(f"Video generation failed: {str(e)}")

async def generate_wav2lip_video(
    audio_url: str,
    video_url: str
) -> str:
    """
    Generate lip-synced video using Wav2Lip model (alternative to SadTalker).
    
    Args:
        audio_url: URL to the audio file
        video_url: URL to the source video
        
    Returns:
        URL to the generated video
    """
    if not settings.REPLICATE_API_TOKEN:
        raise ValueError("REPLICATE_API_TOKEN not set in environment")
    
    try:
        client = replicate.Client(api_token=settings.REPLICATE_API_TOKEN)
        
        output = client.run(
            "devxpy/cog-wav2lip:8d65e3f4f4298520e079198b493c25adfc43c058ffec924f2aefc8010ed25eef",
            input={
                "audio": audio_url,
                "video": video_url
            }
        )
        
        return str(output)
        
    except Exception as e:
        raise Exception(f"Wav2Lip generation failed: {str(e)}")

async def check_generation_status(prediction_id: str) -> dict:
    """
    Check the status of a Replicate prediction.
    
    Args:
        prediction_id: ID of the prediction to check
        
    Returns:
        Status information
    """
    if not settings.REPLICATE_API_TOKEN:
        raise ValueError("REPLICATE_API_TOKEN not set in environment")
    
    url = f"https://api.replicate.com/v1/predictions/{prediction_id}"
    headers = {
        "Authorization": f"Token {settings.REPLICATE_API_TOKEN}"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to check status: {response.text}")
