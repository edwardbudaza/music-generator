import requests
import os

def gen_with_custom_lyrics():
    bearer_token = os.environ.get("API_BEARER_TOKEN")

    if not bearer_token:
        print("Error: API_BEARER_TOKEN environment variable not set")
        return

    headers = {
    "Authorization": f"Bearer {bearer_token}",
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

# ===========================
# MAIN ENTRYPOINT
# ===========================
if __name__ == "__main__":
    gen_with_custom_lyrics()