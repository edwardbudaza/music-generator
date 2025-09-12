import requests
import os


def authentication():
    bearer_token = os.environ.get("API_BEARER_TOKEN")

    if not bearer_token:
        print("Error: API_BEARER_TOKEN environment variable not set")
        return

    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        "https://edwardbudaza--music-generator-musicgenserver-auth-status.modal.run",
        headers=headers
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

# ===========================
# MAIN ENTRYPOINT
# ===========================
if __name__ == "__main__":
    authentication()