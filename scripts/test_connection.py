import os
from pathlib import Path
from dotenv import dotenv_values
from qdrant_client import QdrantClient

env_path = Path(__file__).resolve().parent.parent / '.env'

# Manually load values into a dictionary
config = dotenv_values(env_path)

print(f"File Path: {env_path}")
print(f"Raw Keys Found: {list(config.keys())}")

url = config.get("QDRANT_URL")
key = config.get("QDRANT_API_KEY")

if not url:
    print("ERROR: Key 'QDRANT_URL' not found inside the file. Check for spaces or typos!")
else:
    try:
        client = QdrantClient(url=url, api_key=key)
        client.get_collections()
        print(f"Connection Successful to: {url}")
    except Exception as e:
        print(f"Connection Failed: {e}")