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
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 900px;
        margin: 0 auto;
    }
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
    div[data-testid="stMarkdownContainer"] {
        text-align: center;
    }
    .stHeading {
        text-align: center;
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

# ============ INFO RAPIDE (SUS) ============
st.markdown("## 📊 Informații Rapide")

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

st.markdown("---")

# ============ STIRI (MIJLOC) ============
st.markdown("## 📰 Știri din România")

@st.cache_data(ttl=300)
def fetch_news():
    fallback_news = [
        {
            "title": "Reformă la Romsilva. Ministrul Mediului: Suntem la un pas de a adopta reorganizarea. Trecem de la 41",
            "content": """Reformă la Romsilva. Ministrul Mediului: Suntem la un pas de a adopta reorganizarea. Trecem de la 41, la 19 direcții în toată țara. Află mai multe detalii citind articolul complet.""",
            "category": "Actualitate",
            "url": "https://www.digi24.ro/stiri/actualitate/politica/reforma-la-romsilva-ministrul-mediului-suntem-la-un-pas-de-a-adopta-reorganizarea-trecem-de-la-41-la-19-directii-in-toata-tara-3648457"
        },
        {
            "title": "Exclusiv„Asta ajunge în plămânii noștri”. Diana Buzoianu spune că zăpada neagră de pe străzi este „s",
            "content": """Exclusiv„Asta ajunge în plămânii noștri”. Diana Buzoianu spune că zăpada neagră de pe străzi este „simbolul poluării din București”. Află mai multe detalii citind articolul complet.""",
            "category": "Actualitate",
            "url": "https://www.digi24.ro/stiri/actualitate/politica/asta-ajunge-in-plamanii-nostri-diana-buzoianu-spune-ca-zapada-neagra-de-pe-strazi-este-simbolul-poluarii-din-bucuresti-3648467"
        },
        {
            "title": "Grindeanu face „referendum” în PSD dacă îl mai vrea premier pe Bolojan: „Protocolul poate să rămână ",
            "content": """Grindeanu face „referendum” în PSD dacă îl mai vrea premier pe Bolojan: „Protocolul poate să rămână cu un alt prim-ministru dat de PNL”. Află mai multe detalii citind articolul complet.""",
            "category": "Actualitate",
            "url": "https://www.digi24.ro/stiri/actualitate/politica/grindeanu-face-referendum-in-psd-daca-il-mai-vrea-premier-pe-bolojan-protocolul-poate-sa-ramana-cu-un-alt-prim-ministru-dat-de-pnl-3648443"
        },
        {
            "title": "Un fost șef al poliției din Gorj, pensionar special, numit la conducerea fabricii de armament Sadu. ",
            "content": """Un fost șef al poliției din Gorj, pensionar special, numit la conducerea fabricii de armament Sadu. Explicațiile ministrului Economiei. Află mai multe detalii citind articolul complet.""",
            "category": "Actualitate",
            "url": "https://www.digi24.ro/stiri/actualitate/politica/un-fost-sef-al-politiei-din-gorj-pensionar-special-numit-la-conducerea-fabricii-de-armament-sadu-explicatiile-ministrului-economiei-3648357"
        },
        {
            "title": "Kremlinul pune sub semnul întrebării un summit Putin–Zelenski. Ce piedici invocă",
            "content": """Kremlinul pune sub semnul întrebării un summit Putin–Zelenski. Ce piedici invocă. Află mai multe detalii citind articolul complet.""",
            "category": "Extern",
            "url": "https://www.digi24.ro/stiri/externe/ue/kremlinul-pune-sub-semnul-intrebarii-un-summit-putin-zelenski-ce-piedici-invoca-3648481"
        },
        {
            "title": "Mii de persoane au fost găsite trăind în condiţii „şocante” în centrul de detenţie al-Hol din Siria,",
            "content": """Mii de persoane au fost găsite trăind în condiţii „şocante” în centrul de detenţie al-Hol din Siria, spun autorităţile. Află mai multe detalii citind articolul complet.""",
            "category": "Extern",
            "url": "https://www.digi24.ro/stiri/externe/mii-de-persoane-au-fost-gasite-traind-in-conditii-socante-in-centrul-de-detentie-al-hol-din-siria-spun-autoritatile-3648377"
        },
        {
            "title": "Islanda va organiza în acest an un referendum pentru aderarea la UE, spune şefa guvernului",
            "content": """Islanda va organiza în acest an un referendum pentru aderarea la UE, spune şefa guvernului. Află mai multe detalii citind articolul complet.""",
            "category": "Extern",
            "url": "https://www.digi24.ro/stiri/externe/ue/islanda-va-organiza-in-acest-an-un-referendum-pentru-aderarea-la-ue-spune-sefa-guvernului-3648393"
        },
        {
            "title": "IIF: Cheltuielile guvernamentale au dus datoria mondială la un nivel record în 2025",
            "content": """IIF: Cheltuielile guvernamentale au dus datoria mondială la un nivel record în 2025. Află mai multe detalii citind articolul complet.""",
            "category": "Extern",
            "url": "https://www.digi24.ro/stiri/externe/mapamond/iif-cheltuielile-guvernamentale-au-dus-datoria-mondiala-la-un-nivel-record-in-2025-3648397"
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
