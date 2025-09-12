# Music Generation API Testing Guide

## Your API Endpoints

```
Base URLs:
├── Health Check: https://edwardbudaza--music-generator-musicgenserver-health.modal.run
├── Auth Status: https://edwardbudaza--music-generator-musicgenserver-auth-status.modal.run
├── Simple Generate: https://edwardbudaza--music-generator-musicgenserver-generate.modal.run
├── Generate from Description: https://edwardbudaza--music-generator-musicgenserver-generate-fr-00d3b5.modal.run
├── Generate with Custom Lyrics: https://edwardbudaza--music-generator-musicgenserver-generate-wi-3c63ca.modal.run
└── Generate with Described Lyrics: https://edwardbudaza--music-generator-musicgenserver-generate-wi-f209f5.modal.run

Set Bearer Token: export API_BEARER_TOKEN="************"
```

## 1. Quick Health Check (No Auth Required)

### cURL:
```bash
curl -X GET "https://edwardbudaza--music-generator-musicgenserver-health.modal.run"
```

### Python:
```python
import requests

response = requests.get("https://edwardbudaza--music-generator-musicgenserver-health.modal.run")
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
```

Expected Response:
```json
{
  "status": "healthy",
  "service": "music-generator"
}
```

## 2. Test Authentication

### cURL:
```bash
curl -X POST "https://edwardbudaza--music-generator-musicgenserver-auth-status.modal.run" \
  -H "Authorization: Bearer $API_BEARER_TOKEN" \
  -H "Content-Type: application/json"
```

### Python:
```python
import requests

headers = {
    "Authorization": "Bearer $API_BEARER_TOKEN",
    "Content-Type": "application/json"
}

response = requests.post(
    "https://edwardbudaza--music-generator-musicgenserver-auth-status.modal.run",
    headers=headers
)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
```

## 3. Simple Generate Test (Returns Base64 Audio)

### cURL:
```bash
curl -X POST "https://edwardbudaza--music-generator-musicgenserver-generate.modal.run" \
  -H "Authorization: Bearer $API_BEARER_TOKEN" \
  -H "Content-Type: application/json"
```

### Python:
```python
import requests
import base64

headers = {
    "Authorization": "Bearer $API_BEARER_TOKEN",
    "Content-Type": "application/json"
}

response = requests.post(
    "https://edwardbudaza--music-generator-musicgenserver-generate.modal.run",
    headers=headers
)

if response.status_code == 200:
    result = response.json()
    # Save the audio file
    audio_data = base64.b64decode(result["audio_data"])
    with open("generated_music.wav", "wb") as f:
        f.write(audio_data)
    print("✅ Music generated and saved as 'generated_music.wav'")
else:
    print(f"❌ Error: {response.status_code} - {response.text}")
```

## 4. Generate from Description (Full Pipeline with R2 Upload)

### cURL:
```bash
curl -X POST "https://edwardbudaza--music-generator-musicgenserver-generate-fr-00d3b5.modal.run" \
  -H "Authorization: Bearer $API_BEARER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "full_described_song": "upbeat electronic dance music with heavy bass and energetic beats",
    "audio_duration": 60.0,
    "seed": 42,
    "guidance_scale": 15.0,
    "infer_step": 30,
    "instrumental": false
  }'
```

### Python:
```python
import requests
import json

headers = {
    "Authorization": "Bearer $API_BEARER_TOKEN",
    "Content-Type": "application/json"
}

data = {
    "full_described_song": "upbeat electronic dance music with heavy bass and energetic beats",
    "audio_duration": 60.0,
    "seed": 42,
    "guidance_scale": 15.0,
    "infer_step": 30,
    "instrumental": False
}

response = requests.post(
    "https://edwardbudaza--music-generator-musicgenserver-generate-fr-00d3b5.modal.run",
    headers=headers,
    json=data
)

if response.status_code == 200:
    result = response.json()
    print("✅ Music Generated Successfully!")
    print(f"🎵 Audio R2 Key: {result['r2_key']}")
    print(f"🖼️ Cover Image R2 Key: {result['cover_image_r2_key']}")
    print(f"🏷️ Categories: {', '.join(result['categories'])}")
else:
    print(f"❌ Error: {response.status_code}")
    print(f"Response: {response.text}")
```

## 5. Generate with Custom Lyrics

### cURL:
```bash
curl -X POST "https://edwardbudaza--music-generator-musicgenserver-generate-wi-3c63ca.modal.run" \
  -H "Authorization: Bearer $API_BEARER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "pop rock, guitar driven, upbeat tempo",
    "lyrics": "[verse]\nDancing through the night\nFeeling so alive\nMusic fills the air\nEverything feels right\n\n[chorus]\nThis is our moment\nShining so bright\nNothing can stop us\nWe are the light",
    "audio_duration": 90.0,
    "guidance_scale": 12.0
  }'
```

### Python:
```python
import requests

headers = {
    "Authorization": "Bearer $API_BEARER_TOKEN",
    "Content-Type": "application/json"
}

data = {
    "prompt": "pop rock, guitar driven, upbeat tempo",
    "lyrics": """[verse]
Dancing through the night
Feeling so alive
Music fills the air
Everything feels right

[chorus]
This is our moment
Shining so bright
Nothing can stop us
We are the light""",
    "audio_duration": 90.0,
    "guidance_scale": 12.0
}

response = requests.post(
    "https://edwardbudaza--music-generator-musicgenserver-generate-wi-3c63ca.modal.run",
    headers=headers,
    json=data
)

if response.status_code == 200:
    result = response.json()
    print("✅ Custom Lyrics Music Generated!")
    print(f"🎵 Audio: {result['r2_key']}")
    print(f"🖼️ Cover: {result['cover_image_r2_key']}")
    print(f"🏷️ Categories: {result['categories']}")
else:
    print(f"❌ Error: {response.status_code} - {response.text}")
```

## 6. Generate with Described Lyrics (AI Generates Lyrics)

### cURL:
```bash
curl -X POST "https://edwardbudaza--music-generator-musicgenserver-generate-wi-f209f5.modal.run" \
  -H "Authorization: Bearer $API_BEARER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "acoustic folk, gentle melody, storytelling",
    "described_lyrics": "lyrics about a journey through a magical forest with talking animals",
    "audio_duration": 120.0,
    "seed": 123
  }'
```

### Python:
```python
import requests

headers = {
    "Authorization": "Bearer $API_BEARER_TOKEN",
    "Content-Type": "application/json"
}

data = {
    "prompt": "acoustic folk, gentle melody, storytelling",
    "described_lyrics": "lyrics about a journey through a magical forest with talking animals",
    "audio_duration": 120.0,
    "seed": 123
}

response = requests.post(
    "https://edwardbudaza--music-generator-musicgenserver-generate-wi-f209f5.modal.run",
    headers=headers,
    json=data
)

if response.status_code == 200:
    result = response.json()
    print("✅ AI Lyrics Music Generated!")
    print(f"🎵 Audio: {result['r2_key']}")
    print(f"🖼️ Cover: {result['cover_image_r2_key']}")
    print(f"🏷️ Categories: {result['categories']}")
else:
    print(f"❌ Error: {response.status_code} - {response.text}")
```

## Complete Test Script

Save this as `test_api.py`:

```python
#!/usr/bin/env python3
import requests
import json
import time
import base64
import os

# Configuration
BASE_TOKEN = os.environ.get(API_BEARER_TOKEN)
HEADERS = {
    "Authorization": f"Bearer {BASE_TOKEN}",
    "Content-Type": "application/json"
}

ENDPOINTS = {
    "health": "https://edwardbudaza--music-generator-musicgenserver-health.modal.run",
    "auth": "https://edwardbudaza--music-generator-musicgenserver-auth-status.modal.run",
    "generate": "https://edwardbudaza--music-generator-musicgenserver-generate.modal.run",
    "from_description": "https://edwardbudaza--music-generator-musicgenserver-generate-fr-00d3b5.modal.run",
    "with_lyrics": "https://edwardbudaza--music-generator-musicgenserver-generate-wi-3c63ca.modal.run",
    "described_lyrics": "https://edwardbudaza--music-generator-musicgenserver-generate-wi-f209f5.modal.run"
}

def test_health():
    print("🏥 Testing Health Check...")
    response = requests.get(ENDPOINTS["health"])
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")

def test_auth():
    print("🔐 Testing Authentication...")
    response = requests.post(ENDPOINTS["auth"], headers=HEADERS)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")

def test_simple_generate():
    print("🎵 Testing Simple Generate (this may take a few minutes)...")
    response = requests.post(ENDPOINTS["generate"], headers=HEADERS)
    
    if response.status_code == 200:
        result = response.json()
        # Save audio file
        audio_data = base64.b64decode(result["audio_data"])
        filename = f"simple_generated_{int(time.time())}.wav"
        with open(filename, "wb") as f:
            f.write(audio_data)
        print(f"✅ Music saved as: {filename}\n")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}\n")

def test_from_description():
    print("📝 Testing Generate from Description...")
    data = {
        "full_described_song": "chill lo-fi hip hop with soft piano and vinyl crackle",
        "audio_duration": 30.0,  # Shorter for testing
        "guidance_scale": 15.0,
        "infer_step": 20  # Fewer steps for faster generation
    }
    
    response = requests.post(ENDPOINTS["from_description"], headers=HEADERS, json=data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Generated! R2 Key: {result['r2_key']}")
        print(f"🖼️ Cover: {result['cover_image_r2_key']}")
        print(f"🏷️ Categories: {result['categories']}\n")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}\n")

if __name__ == "__main__":
    print("🚀 Starting API Tests...\n")
    
    # Run tests
    test_health()
    test_auth()
    
    # Uncomment these for full testing (they take longer)
    # test_simple_generate()
    # test_from_description()
    
    print("✅ Basic tests completed!")
```

Run with:
```bash
python test_api.py
```

## Tips for Testing:

1. **Start with health and auth** to ensure everything is working
2. **Use shorter durations** (30-60 seconds) for testing to save time and resources
3. **Lower infer_step values** (20-30) for faster generation during testing
4. **Monitor the Modal logs** in your dashboard for detailed information
5. **Each music generation can take 2-10 minutes** depending on duration and settings
