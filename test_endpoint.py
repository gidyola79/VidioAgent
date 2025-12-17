import requests
import sys

BASE_URL = "http://localhost:8000"

def test_endpoints():
    # 1. Test Root
    try:
        r = requests.get(f"{BASE_URL}/")
        print(f"ROOT: {r.status_code} {r.json()}")
    except Exception as e:
        print(f"ROOT FAILED: {e}")

    # 1.5. Test Inline
    try:
        r = requests.get(f"{BASE_URL}/inline_test")
        print(f"INLINE: {r.status_code} {r.json()}")
    except Exception as e:
        print(f"INLINE FAILED: {e}")

    # 2. Test WhatsApp GET
    try:
        r = requests.get(f"{BASE_URL}/whatsapp/test")
        print(f"WHATSAPP GET: {r.status_code}")
        if r.status_code != 200:
            print(r.text)
    except Exception as e:
        print(f"WHATSAPP GET FAILED: {e}")

    # 3. Test WhatsApp POST
    try:
        data = {"From": "whatsapp:+1234567890", "Body": "Hello"}
        r = requests.post(f"{BASE_URL}/whatsapp/webhook", data=data)
        print(f"WHATSAPP POST: {r.status_code}")
        print(r.text)
    except Exception as e:
        print(f"WHATSAPP POST FAILED: {e}")

    
    # 5. Test Analyze Endpoint (POST)
    print("\nANALYZE POST:")
    try:
        response = requests.post(f"{BASE_URL}/api/analyze", json={
            "name": "Test User",
            "business_type": "Bakery",
            "text": "How can I get more customers?"
        })
        print(response.status_code)
        print(response.json())
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_endpoints()
