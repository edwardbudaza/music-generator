import requests
import base64
import os

def simple_gen():
    bearer_token = os.environ.get("API_BEARER_TOKEN")

    if not bearer_token:
        print("Error: API_BEARER_TOKEN environment variable not set")
        return

    headers = {
        "Authorization": f"Bearer {bearer_token}",
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

# ===========================
# MAIN ENTRYPOINT
# ===========================
if __name__ == "__main__":
    simple_gen()