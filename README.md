# German Law Assistant

A multilingual RAG (Retrieval-Augmented Generation) application that simplifies the German Law for non-lawyers. 

### Features
- **Simple Explanations:** Complex laws explained easily, like you're five.
- **Multilingual:** Ask in any language; the bot responds in your language while citing original German laws.
- **Privacy First:** Uses EU-based Mistral AI (France) and Qdrant (Germany).
- **Custom Knowledge Base:** Uses a vector database of 2,400+ BGB paragraphs. #CHANGE TO ALL WHEN TIME

### Tech Stack
- **Frontend:** [Streamlit](https://streamlit.io/)
- **AI Brain:** [Mistral AI](https://mistral.ai/) (`open-mistral-7b`)
- **Vector Database:** [Qdrant Cloud](https://qdrant.io/)
- **Data Source:** [Gesetze-im-Internet.de](https://www.gesetze-im-internet.de/)

### How to use
1. Visit the [Live Demo](https://german-law-ai.streamlit.app/).
2. Enter your own **Mistral API Key** in the sidebar.
3. Select your preferred explanation language.
4. Ask a question (e.g., "At what age do I become an adult in Germany?").

---
*Disclaimer: This is a student project for educational purposes and does not constitute legal advice.*