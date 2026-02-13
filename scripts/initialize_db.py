import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http import models

# Load environment variables from .env file
load_dotenv()

def setup_database():
    # 1. Connect to Qdrant Cloud Cluster
    client = QdrantClient(
        url=os.getenv('QDRANT_URL'),
        api_key=os.getenv('QDRANT_API_KEY')
    )

    COLLECTION_NAME = "german_laws"

    # 2. Check if collection already exists
    collections = client.get_collections().collections
    exists = any(c.name == COLLECTION_NAME for c in collections)

    if exists:
        print(f"Collection '{COLLECTION_NAME}' already exists. Recreating it for a clean start....")
        client.delete_collection(collection_name=COLLECTION_NAME)

    # 3. Create a collection with correct settings
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(
            size=1024, 
            distance=models.Distance.COSINE
            ),
    )

    print(f"Collection '{COLLECTION_NAME}' created successfully and is ready in the cloud!")

if __name__ == "__main__":
    setup_database()

print(f"Connecting to: {os.getenv('QDRANT_URL')}")