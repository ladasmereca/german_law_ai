import os
from pathlib import Path
from dotenv import load_dotenv
from mistralai import Mistral
from qdrant_client import QdrantClient

env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

def search_law(query_text):
    # 1. Setup Client
    mistral_client = Mistral(api_key=os.getenv('MISTRAL_API_KEY'))
    qdrant_client = QdrantClient(
        url=os.getenv('QDRANT_URL'),
        api_key=os.getenv('QDRANT_API_KEY')
    )

    # 2. Turn the query into embeddings
    print(f"Searching for: {query_text}")
    emb_response = mistral_client.embeddings.create(
        model="mistral-embed",
        inputs=[query_text]
    )
    query_vector = emb_response.data[0].embedding

    # 3. Ask Qdrant to find 3 closest paragraphs
    response = qdrant_client.query_points(
        collection_name="german_laws",
        query=query_vector,
        limit=3
    )

    search_results = response.points

    # 4. Print the results
    print("Search Results:")
    for i, res in enumerate(search_results):
        print(f"\n--- Result {i + 1} (Score: {res.score:.4f}) ---")
        print(f"Law: {res.payload['id']} - {res.payload['title']}")
        print(f"Text: {res.payload['text'][:200]}") # Print first 200 characters

if __name__ == "__main__":
    search_law("At what age can I vote?")