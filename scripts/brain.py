import os
from pathlib import Path
from dotenv import load_dotenv
from mistralai import Mistral
from qdrant_client import QdrantClient
import streamlit as st

env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

def ask_legal_bot(question, user_api_key, language):
    # 1. Setup Client
    mistral_client = Mistral(api_key=user_api_key)
    qdrant_client = QdrantClient(
        url=st.secrets["QDRANT_URL"],
        api_key=st.secrets["QDRANT_API_KEY"]
    )

    # 2. Search the law
    emb_response = mistral_client.embeddings.create(
        model="mistral-embed",
        inputs=[question]
    )
    query_vector = emb_response.data[0].embedding

    search_results = qdrant_client.query_points(
        collection_name="german_laws",
        query=query_vector,
        limit=3
    ).points

    # Check if the best result is a good match
    if not search_results or search_results[0].score < 0.6:
        return "I am sorry, I couldn't find a relevant law to answer your question. Please try again with a different question."

    # 3. Extract text from search results
    context = ""
    for res in search_results:
        context += f"\n Law: {res.payload['id']} ({res.payload['title']}): {res.payload['text']}\n"

    # 4. Create Prompt
    prompt = f"""
    ROLE: Specialized legal assistant for the German Law.
    You have access to a verified database of German laws.
    
    CONTEXT FROM DATABASE: {context}
    USER QUESTION: {question}

    STRICT RULES:
    - Answer strictly in {language}.
    - Keep law titles in German (e.g., '§ 433 BGB Vertragstypische Pflichten beim Kaufvertrag'). Always base your answer on the law.
    - If the question is outside of German law, explain the {context} range and that you cannot answer questions outside of German law. 
    - If it is about German law, but you can't find any corresponding laws in {context}, explain it to the user.
    - Answer in {language} - this is the language of the user.
    - Style: Simple (ELI5), no emojis.
    """

    # 5. Generate explanation
    response = mistral_client.chat.complete(
        model="open-mistral-7b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content

# if __name__ == "__main__":
#     user_q = "What is the legal age to vote?"
#     answer = ask_legal_bot(user_q)
#     print(answer)