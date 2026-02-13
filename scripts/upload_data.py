import os
import time
from pathlib import Path
from dotenv import load_dotenv
from mistralai import Mistral
from qdrant_client import QdrantClient
from qdrant_client.http import models
from xml_parser import parse_xml

# Load .env from the root folder
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

def upload_laws():
    # 1. Setup Client
    mistral_client = Mistral(api_key=os.getenv('MISTRAL_API_KEY'))
    qdrant_client = QdrantClient(
        url=os.getenv('QDRANT_URL'),
        api_key=os.getenv('QDRANT_API_KEY')
    )

    COLLECTION_NAME = "german_laws"

    # 2. Parse XML and get law chunks
    print("Parsing XML...")
    chunks = parse_xml('data/BGB.xml')
    print(f"Successfully parsed {len(chunks)} law sections.")

    # 3. Process in batches
    batch_size = 50
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        
        # Extract text for Mistral
        texts = [item['text'] for item in batch]

        try:
            print(f"Vectorising & uploading batch {i // batch_size + 1}...")

            # Get embeddings from Mistral
            emb_response = mistral_client.embeddings.create(
                model="mistral-embed",
                inputs=texts
            )

            # Prepare points for Qdrant
            points = []
            for j, item in enumerate(batch):
                points.append(
                    models.PointStruct(
                        id=i + j, # Assign IDs to each point
                        vector=emb_response.data[j].embedding,
                        payload=item #Store title, paragraph number, and text
                    )
                )
            # Upload to Qdrant
            qdrant_client.upsert(
                collection_name=COLLECTION_NAME,
                points=points
            )
            
            time.sleep(1)

        except Exception as e:
            print(f"An error occurred in batch {i // batch_size + 1} {e}")
            continue

    print(f"Successfully uploaded {len(chunks)} law sections to Qdrant!")

if __name__ == "__main__":
    upload_laws()