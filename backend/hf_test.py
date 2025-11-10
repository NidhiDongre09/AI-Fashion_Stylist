import requests, base64, os
from dotenv import load_dotenv
load_dotenv()

hf_api_key = os.getenv("HUGGINGFACE_API_KEY")
prompt = "a fashionable outfit for a summer evening"

headers = {"Authorization": f"Bearer {hf_api_key}"}
payload = {"inputs": prompt}

url = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"

response = requests.post(url, headers=headers, json=payload)

print("Status:", response.status_code)
print("Response:", response.text[:300])
