import json
import requests

from config import settings

response = requests.get(
    "https://api.smallest.ai/waves/v1/lightning-v3.1/get_voices",
    headers={
        "Authorization": f"Bearer {settings.smallest_api_key}",
    },
)

response.raise_for_status()

data = response.json()

voices = data["voices"] if isinstance(data, dict) and "voices" in data else data

print(json.dumps(voices[0], indent=2, ensure_ascii=False))