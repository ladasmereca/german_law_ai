import streamlit as st
from scripts.brain import ask_legal_bot

# CSS design
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Source+Serif+Pro:wght@400;700&family=Inter:wght@400;600&display=swap');

    /* 1. Main background */
    .stApp {
        background-color: #FDFCFB;
    }

    /* 2. AI Assistant Message Styling */
    div[data-testid="stChatMessageAssistant"] {
        font-family: 'Source Serif Pro', serif !important;
        background-color: #F4F1EA !important;
        border-left: 5px solid #8B4513 !important;
        color: #2C2621 !important;
    }

    /* 3. Global Interface Font */
    html, body, [class*="css"], .stMarkdown {
        font-family: 'Inter', sans-serif;
    }

    /* 4. Sidebar - Main Container */
    section[data-testid="stSidebar"] {
        background-color: #2C2621 !important;
    }

    /* 5. Sidebar - Text & Headers (Fixes the Blue 'Settings' text) */
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] .stMarkdown, 
    section[data-testid="stSidebar"] label, 
    section[data-testid="stSidebar"] p {
        color: #E6D5B8 !important;
    }

    /* 6. Sidebar - Expander Headers (Specifically targeting the clickable text) */
    section[data-testid="stSidebar"] details summary span p {
        color: #E6D5B8 !important;
    }

    section[data-testid="stSidebar"] details summary svg {
        fill: #E6D5B8 !important; /* Makes the little arrow icon cream colored too */
    }

    /* 7. Main Title Header (Center Page) */
    .main-header {
        font-family: 'Source Serif Pro', serif;
        color: #5D4037;
        font-weight: 700;
        font-size: 2.2rem;
    }

    /* 8. Links Styling */
    .footer-link {
        color: #D4A373 !important;
        text-decoration: underline;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. UI Setup
translations = {
    "English": {
        "title": "German Law AI Assistant",
        "warning": "**DISCLAIMER:** This is a student project and NOT legal advice.",
        "sidebar_head": "Settings",
        "lang_select": "Explanation Language",
        "key_label": "Enter your Mistral API-Key",
        "key_info": "Please add your Mistral API-key to continue.",
        "placeholder": "Ask a question...",
        "footer":'Developed by Lada S. | <a class="footer-link" href="https://github.com/">GitHub Repo</a><br>' \
                'AI Powered by <a class="footer-link" href="https://mistral.ai">Mistral</a><br>' \
                'Database Powered by <a class="footer-link" href="https://qdrant.io">Qdrant</a><br>' \
                'Laws taken from <a class="footer-link" href="https://www.gesetze-im-internet.de/">Gesetze-in-Internet.de</a>'
    },
    "German": {
        "title": "Deutscher Rechts-KI-Assistent",
        "warning": "**HAFTUNGSAUSSCHLUSS:** Dies ist ein Studentenprojekt und KEINE Rechtsberatung.",
        "sidebar_head": "Einstellungen",
        "lang_select": "Erklärungssprache",
        "key_label": "Geben Sie Ihren Mistral API-Key ein",
        "key_info": "Bitte fügen Sie Ihren Mistral API-Key hinzu, um fortzufahren.",
        "placeholder": "Stellen Sie eine Frage...",
        "footer":'Entwickelt von Lada S. | <a class="footer-link" href="https://github.com/">GitHub Repo</a><br>' \
                'KI-Unterstützung durch <a class="footer-link" href="https://mistral.ai">Mistral</a><br>' \
                'Datenbankunterstützung durch <a class="footer-link" href="https://qdrant.io">Qdrant</a><br>' \
                'Gesetze übernommen von <a class="footer-link" href="https://www.gesetze-im-internet.de/">Gesetze-in-Internet.de</a>'
    },
    "Polish": {
        "title": "Asystent AI prawa niemieckiego",
        "warning": "**ZASTRZEŻENIE:** Jest to projekt studencki i NIE stanowi porady prawnej.",
        "sidebar_head": "Ustawienia",
        "lang_select": "Język wyjaśnienia",
        "key_label": "Wprowadź swój Mistral API-Key",
        "key_info": "Aby kontynuować, dodacj swój Mistral API-key.",
        "placeholder": "Zadaj pytanie...",
        "footer":'Opracowane przez Lada S. | <a class="footer-link" href="https://github.com/">GitHub Repo</a><br>' \
                'AI oparta na <a class="footer-link" href="https://mistral.ai">Mistral</a><br>' \
                'Baza danych oparta na <a class="footer-link" href="https://qdrant.io">Qdrant</a><br>' \
                'Przepisy prawne zaczerpnięte z <a class="footer-link" href="https://www.gesetze-im-internet.de/">Gesetze-in-Internet.de</a>'
    },
    "Turkish": {
        "title": "Alman Hukuku AI Asistanı",
        "warning": "**YASAL UYARI:** Bu bir öğrenci projesidir ve hukuki tavsiye niteliği taşımaz.",
        "sidebar_head": "Ayarlar",
        "lang_select": "Açıklama Dili",
        "key_label": "Mistral API Anahtarınızı girin",
        "key_info": "Devam etmek için lütfen Mistral API anahtarınızı ekleyin.",
        "placeholder": "Bir soru sorun...",
        "footer":'Lada S. tarafından geliştirilmiştir | <a class="footer-link" href="https://github.com/">GitHub Repo</a><br>' \
                'AI tarafından desteklenmektedir <a class="footer-link" href="https://mistral.ai">Mistral</a><br>' \
                'Veritabanı tarafından desteklenmektedir <a class="footer-link" href="https://qdrant.io">Qdrant</a><br>' \
                'Yasalar adresinden alınmıştır <a class="footer-link" href="https://www.gesetze-im-internet.de/">Gesetze-in-Internet.de</a>'
    },
    "Ukrainian": {
        "title": "AI-помічник для німецького права",
        "warning": "**ПРИМІТКА:** Це студентський проєкт і НЕ є юридичною порадою.",
        "sidebar_head": "Налаштування",
        "lang_select": "Мова опису",
        "key_label": "Введіть Mistral API-ключ",
        "key_info": "Для продовження, додайте Mistral API-ключ.",
        "placeholder": "Задайте питання...",
        "footer":'Розроблено Lada S. | <a class="footer-link" href="https://github.com/">GitHub Repo</a><br>' \
                'AI на базі <a class="footer-link" href="https://mistral.ai">Mistral</a><br>' \
                'База даних на базі <a class="footer-link" href="https://qdrant.io">Qdrant</a><br>' \
                'Закони взяті з <a class="footer-link" href="https://www.gesetze-im-internet.de/">Gesetze-in-Internet.de</a>'
    },
    "Romanian": {
        "title": "Asistent AI pentru legislația germană",
        "warning": "**DECLARAȚIE DE RESPONSABILITATE:** Acesta este un proiect studențesc și NU constituie consultanță juridică.",
        "sidebar_head": "Setări",
        "lang_select": "Limba explicației",
        "key_label": "Introduceți cheia API Mistral",
        "key_info": "Adăugați cheia API Mistral pentru a continua.",
        "placeholder": "Puneți o întrebare...",
        "footer":'Dezvoltat de Lada S. | <a class="footer-link" href="https://github.com/">GitHub Repo</a><br>' \
                'AI alimentat de <a class="footer-link" href="https://mistral.ai">Mistral</a><br>' \
                'Baza de date alimentată de <a class="footer-link" href="https://qdrant.io">Qdrant</a><br>' \
                'Legi preluate de pe <a class="footer-link" href="https://www.gesetze-im-internet.de/">Gesetze-in-Internet.de</a>'
    },
    "Arabic": {
        "title": "مساعد الذكاء الاصطناعي للقانون الألماني",
        "warning": "**إخلاء المسؤولية:** هذا مشروع طلابي وليس مشورة قانونية.",
        "sidebar_head": "الإعدادات",
        "lang_select": "لغة الشرح",
        "key_label": "أدخل مفتاح API Mistral الخاص بك",
        "key_info": "يرجى إضافة مفتاح API Mistral الخاص بك للمتابعة.",
        "placeholder": "اطرح سؤالاً...",
        "footer":'Lada S. تم تطويره بواسطة | <a class="footer-link" href="https://github.com/">GitHub Repo</a><br>' \
                'الذكاء الاصطناعي مدعوم من <a class="footer-link" href="https://mistral.ai">Mistral</a><br>' \
                'قاعدة البيانات مدعومة من <a class="footer-link" href="https://qdrant.io">Qdrant</a><br>' \
                'القوانين مأخوذة من <a class="footer-link" href="https://www.gesetze-im-internet.de/">Gesetze-in-Internet.de</a>'
    },
    "Russian": {
        "title": "AI-помощник для немецкого права",
        "warning": "**ПРЕДУПРЕЖДЕНИЕ:** Это студенческий проект и НЕ является юридической консультацией.",
        "sidebar_head": "Настройки",
        "lang_select": "Язык описания",
        "key_label": "Введите Mistral API-ключ",
        "key_info": "Для продолжения, добавьте Mistral API-ключ.",
        "placeholder": "Задайте вопрос...",
        "footer": 'Разработан Lada S. | <a class="footer-link" href="https://github.com/">GitHub Repo</a><br>' \
                'AI на базе <a class="footer-link" href="https://mistral.ai">Mistral</a><br>' \
                'База данных на базе <a class="footer-link" href="https://qdrant.io">Qdrant</a><br>' \
                'Законы взяты из <a class="footer-link" href="https://www.gesetze-im-internet.de/">Gesetze-in-Internet.de</a>'
    }
}

# 2. Sidebar
with st.sidebar:
    lang_display = {
        "English": "English 🇬🇧", 
        "German": "Deutsch 🇩🇪", 
        "Polish": "Polish 🇵🇱",
        "Turkish": "Türkçe 🇹🇷", 
        "Ukrainian": "Українська 🇺🇦", 
        "Romanian": "Română 🇷🇴",
        "Arabic": "العربية 🇦🇪", 
        "Russian": "Pусский 🇷🇺"
    }
    selected_lang = st.selectbox("Language / Sprache", list(lang_display.keys()), format_func=lambda x: lang_display[x])
    t = translations.get(selected_lang, translations["English"])

    st.header(t["sidebar_head"])
    user_mistral_key = st.text_input(t["key_label"], type="password")

    st.divider()

    # Mistral Key Instructions
    with st.expander("How do I get my Mistral API-Key? (It's free!)"):
            st.markdown("""
            **Only takes a minute and is free for new accounts:**
            1. **Create your account:** Visit the [Mistral AI website](https://console.mistral.ai/) and sign up.
            2. **Get your key:** On the left side, look for a button that says **'API Keys'**. Click the 'Create New Key' button.
            3. **Copy & Paste:** Copy that long code and paste it into the box above.
            
            **Good to know:**
            * Your key is like a password—keep it safe! If you lose it, you can just create a new one.
            * Mistral gives you **free trial credits**. If the bot stops responding later, it likely means the credits ran out. You can check your usage on their website anytime (API Keys -> Usage)!
            """)

    with st.expander("Found a Bug? / Suggestion?"):
        st.link_button("Submit Feedback", "https://tally.so/r/your-link")

    st.markdown("---")
    st.markdown(f"<div style='font-size: 12px; color: #E6D5B8;'>{t['footer']}</div>", unsafe_allow_html=True)

# 3. Main UI
st.markdown(f'<h1 class="main-header">⚖️ {t["title"]}</h1>', unsafe_allow_html=True)
st.warning(t["warning"])

if not user_mistral_key:
    st.info(t["key_info"])
    st.stop()

# 4. Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. User Input
if prompt := st.chat_input(t["placeholder"]):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing legal database..."):
            # Passing key and language
            answer = ask_legal_bot(
                question=prompt,
                user_api_key=user_mistral_key,
                language=selected_lang
            )
            st.markdown(answer)
    # Add response to history
    st.session_state.messages.append({"role": "assistant", "content": answer})