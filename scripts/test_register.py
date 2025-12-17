import requests
import io

API_URL = "http://127.0.0.1:8000"
endpoint = f"{API_URL}/api/business/register"

data = {
    "name": "Test Bakery",
    "whatsapp_number": "+1234567890",
    "owner_name": "Test Owner",
    "business_type": "Bakery",
    "response_style": "friendly",
    "password": "Password123!",
}

# Create tiny dummy files in memory
files = {
    "voice_sample": ("voice.wav", io.BytesIO(b"RIFFTESTAUDIO"), "audio/wav"),
    "avatar_image": ("avatar.jpg", io.BytesIO(b"\xff\xd8\xffTESTJPEG"), "image/jpeg"),
}

print("Posting test registration to:", endpoint)
try:
    resp = requests.post(endpoint, data=data, files=files, timeout=30)
    print("Status:", resp.status_code)
    try:
        print("JSON:", resp.json())
    except Exception:
        print("Text:", resp.text)
except Exception as e:
    print("Request failed:", repr(e))
