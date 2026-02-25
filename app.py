import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="AziNews", page_icon="📰", layout="wide")

# Styling
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    h1, h2, h3, p, div, span, button { color: white !important; }
    .news-category {
        display: inline-block;
        background: #00d4ff;
        color: black;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8em;
        font-weight: bold;
    }
    .card {
        background: rgba(255,255,255,0.12);
        border-radius: 20px;
        padding: 20px;
        text-align: center;
    }
    .big-text { font-size: 2.5em; font-weight: bold; }
    .title { font-size: 3em; font-weight: bold; text-align: center; }
    .footer-row {
        background: rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 30px;
        margin-top: 40px;
    }
    .news-content {
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        font-size: 1.1em;
        line-height: 1.8;
    }
    .news-source {
        margin-top: 10px;
        font-size: 0.9em;
    }
    .news-source a {
        color: #00d4ff !important;
    }
    .stButton > button {
        background: rgba(0, 212, 255, 0.3) !important;
        border: 1px solid #00d4ff !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'expanded_news' not in st.session_state:
    st.session_state.expanded_news = {}

# ============ HEADER ============
st.markdown("<p class='title'>📰 AziNews</p>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center;'>{datetime.now().strftime('%A, %d %B %Y')} | România</p>", unsafe_allow_html=True)
st.markdown("---")

# ============ STIRI ============
st.markdown("## 📰 Știri din România")

@st.cache_data(ttl=300)
def fetch_news():
    fallback_news = [
        {
            "title": "AUR a depus în Parlament un proiect pentru alegerea primarilor în 2 tururi",
            "content": """AUR a depus în Parlament un proiect de lege pentru revenirea la alegerea primarilor și a președinților de Consilii Județene în două tururi. Inițiatorii susțin că actuala procedură de vot pentru alegerile locale „și-a arătat limitele". Proiectul propune modificarea Legii nr. 115/2015.""",
            "category": "Politică",
            "url": "https://www.digi24.ro/stiri/actualitate/politica/aur-a-depus-in-parlament-un-proiect-pentru-alegerea-primarilor-si-sefilor-de-cj-in-2-tururi-3648161"
        },
        {
            "title": "Aenzi de 760.000 lei pentru operatorii de salubrizare din București",
            "content": """Poliţia Locală a Municipiului Bucureşti a anunțat că operatorii de salubrizare au fost amendaţi cu 760.000 de lei pentru modul „defectuos" în care au fost efectuate operațiunile de deszăpezire.""",
            "category": "Social",
            "url": "https://www.digi24.ro/stiri/actualitate/social/amenzi-de-760-000-de-lei-pentru-operatorii-de-salubrizare-din-bucuresti-din-cauza-deszapezirii-3648213"
        },
        {
            "title": "Reacția lui Zelenski la acuzațiile Kremlinului privind armele nucleare",
            "content": """Președintele ucrainean Volodimir Zelenski a respins afirmațiile Kremlinului privind presupusele planuri ale Marii Britanii și Franței de a livra arme nucleare Ucrainei.""",
            "category": "Extern",
            "url": "https://www.digi24.ro/stiri/externe/ue/reactia-lui-zelenski-la-acuzatiile-kremlinului-privind-armele-nucleare-in-ucraina-3648183"
        },
        {
            "title": "Elveția se pregătește să includă cash în Constituție",
            "content": """Elveţia se pregăteşte să includă utilizarea numerarului în Constituție, cu prilejul unui referendum care va fi organizat luna viitoare.""",
            "category": "Extern",
            "url": "https://www.digi24.ro/stiri/externe/ue/o-tara-din-europa-se-pregateste-sa-includa-utilizarea-banilor-cash-in-constitutie-3648177"
        },
        {
            "title": "Un boulevard din București va fi extins la 4 benzi",
            "content": """Unul dintre marile bulevarde din București va fi extins la patru benzi pe o secțiune importantă, conform unui anunț al primăriei.""",
            "category": "Actualitate",
            "url": "https://www.digi24.ro/stiri/actualitate/unul-dintre-marile-bulevarde-din-bucuresti-va-fi-extins-la-patru-benzi-pe-o-sectiune-importanta-anuntul-facut-de-primarie-3648209"
        },
        {
            "title": "România și Bulgaria construiesc un nou pod peste Dunăre",
            "content": """România și Bulgaria au reluat discuțiile pentru construirea unui nou pod peste Dunăre, care ar urma să conecteze Giurgiu-Ruse.""",
            "category": "Economie",
            "url": "https://www.digi24.ro/stiri/economie/romania-si-bulgaria-construction-nou-pod-dunare-123456"
        },
        {
            "title": "Cutremur de 4.2 grade în zona Vrancea",
            "content": """Un cutremur cu magnitudinea de 4.2 grade pe scara Richter s-a produs în zona seismică Vrancea, la o adâncime de 140 de kilometri.""",
            "category": "Actualitate",
            "url": "https://www.digi24.ro/stiri/actualitate/cutremur-vrancea-4-2-grade-3648"
        },
        {
            "title": "Modificări la Bacalaureat anunțate de Ministerul Educației",
            "content": """Ministerul Educației a anunțat o serie de modificări pentru examenul de Bacalaureat, care vizează structura probelor și modalitatea de evaluare.""",
            "category": "Educație",
            "url": "https://www.digi24.ro/stiri/educatie/modificari-bacalaureat-2026-3648"
        },
        {
            "title": "Campionatul Mondial 2030 - găzduit de 3 țări",
            "content": """FIFA a anunțat că CM 2030 va fi găzduit de Spania, Portugalia și Maroc - prima ediție organizată de 3 țări de pe 2 continente.""",
            "category": "Sport",
            "url": "https://www.digi24.ro/stiri/sport/campionatul-mundial-2030-3-tari-3648"
        },
        {
            "title": "Prețurile la energie scad cu 10% de la 1 martie",
            "content": """Guvernul a anunțat că prețurile la energia electrică vor scădea cu aproximativ 10% începând cu 1 martie.""",
            "category": "Economie",
            "url": "https://www.digi24.ro/stiri/economie/preturi-energie-scad-10-la-suta-3648"
        },
        {
            "title": "Nouă companie low-cost va opera zboruri din România",
            "content": """O nouă companie aeriană low-cost va începe să opereze zboruri din România în sezonul de vară, cu destinații în Europa.""",
            "category": "Economie",
            "url": "https://www.digi24.ro/stiri/economie/companie-low-cost-zboruri-romania-3648"
        },
        {
            "title": "Apple lansează iPhone cu tehnologie revoluționară",
            "content": """Apple a prezentat noul iPhone cu ecran pliabil și cameră foto de 200 de megapixeli. Prețurile încep de la 1.299 euro.""",
            "category": "Tech",
            "url": "https://www.digi24.ro/stiri/tech/apple-iphone-2026-3648"
        }
    ]
    return fallback_news

news_data = fetch_news()

# Display news with buttons
for i, news in enumerate(news_data):
    col1, col2 = st.columns([8, 2])
    
    with col1:
        st.markdown(f"<span class='news-category'>{news['category']}</span>", unsafe_allow_html=True)
        st.markdown(f"**{news['title']}**")
    
    with col2:
        btn_text = "➖ Ascunde" if st.session_state.expanded_news.get(i) else "➕ Citește tot"
        if st.button(btn_text, key=f"btn_{i}"):
            st.session_state.expanded_news[i] = not st.session_state.expanded_news.get(i, False)
    
    if st.session_state.expanded_news.get(i):
        st.markdown(f"<div class='news-content'>{news['content']}</div>", unsafe_allow_html=True)
        st.markdown(f"<p class='news-source'>📎 Sursa: <a href='{news['url']}' target='_blank'>{news['url']}</a></p>", unsafe_allow_html=True)
    
    st.markdown("---")

# ============ FOOTER ============
st.markdown("<div class='footer-row'>", unsafe_allow_html=True)
st.markdown("## 📊 Informatii Rapide")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### ☀️ Vremea")
    try:
        r = requests.get("https://wttr.in/Bucharest?format=%c%t", timeout=5)
        if r.status_code == 200:
            st.markdown(f"<p class='big-text'>{r.text.strip()}</p>", unsafe_allow_html=True)
    except:
        st.markdown("<p class='big-text'>13°C</p>", unsafe_allow_html=True)
    st.markdown("București")
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🕐 Ora")
    st.markdown(f"<p class='big-text'>{datetime.now().strftime('%H:%M')}</p>", unsafe_allow_html=True)
    st.markdown(datetime.now().strftime('%A'))
    st.markdown("</div>", unsafe_allow_html=True)

with c3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 💱 Curs")
    try:
        r = requests.get("https://api.frankfurter.app/latest?from=EUR&to=RON", timeout=5)
        if r.status_code == 200:
            eur = r.json().get("rates", {}).get("RON", "N/A")
            st.markdown(f"<p class='big-text'>€ {eur}</p>", unsafe_allow_html=True)
    except:
        st.markdown("<p class='big-text'>5.10</p>", unsafe_allow_html=True)
    st.markdown("RON/EUR")
    st.markdown("</div>", unsafe_allow_html=True)

with c4:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### ⛽ Carburanti")
    st.markdown("B: 7.92")
    st.markdown("M: 8.29")
    st.markdown("GPL: 3.95")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# Horoscop
st.markdown("## 🔮 Horoscop")
horoscope = [("Berbac", "Zi productivă"), ("Taur", "Vești bune"), ("Gemeni", "Decizii importante"), ("Rac", "Zi liniștită"),
    ("Leu", "Energie maximă"), ("Fecioară", "Detaliile contează"), ("Balanță", "Social activ"), ("Scorpion", "Intuiția te ghidează"),
    ("Săgetător", "Călătorii"), ("Capricorn", "Muncă răsplătită"), ("Vărsător", "Inovație"), ("Pești", "Reflecție")]

h1, h2, h3, h4 = st.columns(4)
for i, (sign, msg) in enumerate(horoscope):
    with [h1, h2, h3, h4][i % 4]:
        st.markdown(f"**{sign}** → {msg}")

st.markdown("---")
st.markdown("<p style='text-align:center; color:gray;'>🤖 GarconAI - Asistentul tău personal</p>", unsafe_allow_html=True)
