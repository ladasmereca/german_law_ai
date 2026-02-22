# German Law Assistant

A multilingual RAG (Retrieval-Augmented Generation) application designed to make the German Civil Code (BGB) accessible to international residents and non-lawyers. 

### Features
- **Simple Explanations:** Complex legal jargon translated into simple, actionable insights.
- **Multilingual Support:** Navigate German law in 8+ languages (English, German, Polish, Turkish, Ukrainian, Romanian, Arabic, Russian).
- **Custom Knowledge Base:** Uses a vector database of 2,400+ BGB paragraphs.
- **Heritage-Inspired UI:** A "grounded" interface designed with custom CSS to build user trust and professional credibility.
- **Privacy First:** Uses EU-based Mistral AI (France) and Qdrant (Germany).

### Tech Stack
- **Frontend:** [Streamlit](https://streamlit.io/) + Custom CSS
- **AI Brain:** [Mistral AI](https://mistral.ai/) (`open-mistral-7b`)
- **Vector Database:** [Qdrant Cloud](https://qdrant.io/)
- **Data Source:** [Gesetze-im-Internet.de](https://www.gesetze-im-internet.de/) (XML Parsing)

### How to use
1. Visit the [Live Demo](https://german-law-ai.streamlit.app/).
2. Enter your own **Mistral API Key** in the sidebar.
3. Select your preferred explanation language.
4. Ask a question (e.g., "At what age do I become an adult in Germany?").


### Technical Improvements (v.1.1)
- **State-Aware Multilingual Logic:** Optimized Streamlit session state to handle seamless language switching without data loss or application crashes.
- **Contextual Guardrails:** Engineered a "self-aware" prompt system that identifies the current database scope (e.g., BGB) to prevent AI hallucinations and ensure information is only drawn from verified legal sources.
- **Metadata Attribution:** The assistant programmatically identifies and cites specific law titles and paragraph numbers from the vector database.

### Roadmap
- [ ] Add GG (Basic Law) and StGB (Penal Code) to the knowledge base.
- [ ] Implement automatic uploads of new laws.
- [ ] Add in AI Agent to doublecheck the answers.

---
*Disclaimer: This is a student project for educational purposes and does not constitute legal advice. It is a tool for orientation, not a replacement for professional legal counsel.*
