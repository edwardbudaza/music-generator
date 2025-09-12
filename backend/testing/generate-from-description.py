import requests
import json
import os

def generate_from_desc():
    bearer_token = os.environ.get("API_BEARER_TOKEN")

    if not bearer_token:
        print("Error: API_BEARER_TOKEN environment variable not set")
        return

    headers = {
        "Authorization": f"Bearer {bearer_token}",
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

# ===========================
# MAIN ENTRYPOINT
# ===========================
if __name__ == "__main__":
    generate_from_desc()