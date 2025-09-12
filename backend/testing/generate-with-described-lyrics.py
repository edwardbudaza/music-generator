import requests
import os

def gen_with_desc_lyrics():
    bearer_token = os.environ.get("API_BEARER_TOKEN")

    if not bearer_token:
        print("Error: API_BEARER_TOKEN environment variable not set")
        return

    headers = {
        "Authorization": f"Bearer {bearer_token}",
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

# ===========================
# MAIN ENTRYPOINT
# ===========================
if __name__ == "__main__":
    gen_with_desc_lyrics()