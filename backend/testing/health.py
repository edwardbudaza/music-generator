import requests

response = requests.get("https://edwardbudaza--music-generator-musicgenserver-health.modal.run")
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")