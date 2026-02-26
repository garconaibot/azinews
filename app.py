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
        padding-top: 1rem;
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
            "title": "Desemnarea noilor șefi de parchete. Cei cinci candidați pentru funcţia de procuror-şef adjunct al DI",
            "content": """Desemnarea noilor șefi de parchete. Cei cinci candidați pentru funcţia de procuror-şef adjunct al DIICOT, intervievați astăzi. Află mai multe detalii citind articolul complet.""",
            "category": "Actualitate",
            "url": "https://www.digi24.ro/stiri/actualitate/justitie/desemnarea-noilor-sefi-de-parchete-cei-cinci-candidati-pentru-functia-de-procuror-sef-adjunct-al-diicot-intervievati-astazi-3648711"
        },
        {
            "title": "VideoIlie Bolojan, vizită oficială la Bruxelles: premierul va discuta cu Ursula von der Leyen despre",
            "content": """VideoIlie Bolojan, vizită oficială la Bruxelles: premierul va discuta cu Ursula von der Leyen despre PNRR. Agenda deplasării. Află mai multe detalii citind articolul complet.""",
            "category": "Actualitate",
            "url": "https://www.digi24.ro/stiri/actualitate/politica/ilie-bolojan-vizita-oficiala-la-bruxelles-premierul-va-discuta-cu-ursula-von-der-leyen-despre-pnrr-agenda-deplasarii-3648699"
        },
        {
            "title": "Cine este astronautul din cauza căruia a fost evacuat întreg echipajul de pe Staţia Spaţială Interna",
            "content": """Cine este astronautul din cauza căruia a fost evacuat întreg echipajul de pe Staţia Spaţială Internaţională. „Mă simt foarte bine”. Află mai multe detalii citind articolul complet.""",
            "category": "Actualitate",
            "url": "https://www.digi24.ro/stiri/externe/sua/cine-este-astronautul-din-cauza-caruia-a-fost-evacuat-intreg-echipajul-de-pe-statia-spatiala-internationala-ma-simt-foarte-bine-3648533"
        },
        {
            "title": "Expunerea la zgomotul din trafic în timpul somnului este asociată cu creșterea „colesterolului rău”,",
            "content": """Expunerea la zgomotul din trafic în timpul somnului este asociată cu creșterea „colesterolului rău”, arată un studiu european. Află mai multe detalii citind articolul complet.""",
            "category": "Actualitate",
            "url": "https://www.digi24.ro/stiri/actualitate/sanatate/expunerea-la-zgomotul-din-trafic-in-timpul-somnului-este-asociata-cu-cresterea-colesterolului-rau-arata-un-studiu-european-3648401"
        },
        {
            "title": "Video„A încetat să mai existe”. Ucrainenii le-au distrus rușilor un lansator de rachete S-400 și un ",
            "content": """Video„A încetat să mai existe”. Ucrainenii le-au distrus rușilor un lansator de rachete S-400 și un sistem Panțir în Crimeea ocupată ilegal. Află mai multe detalii citind articolul complet.""",
            "category": "Extern",
            "url": "https://www.digi24.ro/stiri/externe/a-incetat-sa-mai-existe-ucrainenii-le-au-distrus-rusilor-un-lansator-de-rachete-s-400-si-un-sistem-pantir-in-crimeea-ocupata-ilegal-3648595"
        },
        {
            "title": "Cine este astronautul din cauza căruia a fost evacuat întreg echipajul de pe Staţia Spaţială Interna",
            "content": """Cine este astronautul din cauza căruia a fost evacuat întreg echipajul de pe Staţia Spaţială Internaţională. „Mă simt foarte bine”. Află mai multe detalii citind articolul complet.""",
            "category": "Extern",
            "url": "https://www.digi24.ro/stiri/externe/sua/cine-este-astronautul-din-cauza-caruia-a-fost-evacuat-intreg-echipajul-de-pe-statia-spatiala-internationala-ma-simt-foarte-bine-3648533"
        },
        {
            "title": "Cum i-a întins Deutsche Bank covorul roșu lui Jeffrey Epstein: unul dintre cei mai sofisticați, dar ",
            "content": """Cum i-a întins Deutsche Bank covorul roșu lui Jeffrey Epstein: unul dintre cei mai sofisticați, dar și mai dificili clienți. Află mai multe detalii citind articolul complet.""",
            "category": "Extern",
            "url": "https://www.digi24.ro/stiri/externe/sua/cum-i-a-intins-deutsche-bank-covorul-rosu-lui-jeffrey-epstein-unul-dintre-cei-mai-sofisticati-dar-si-mai-dificili-clienti-3647827"
        },
        {
            "title": "Ce s-a întâmplat după ce Elon Musk a deconectat armata rusă de la rețeaua Starlink",
            "content": """Ce s-a întâmplat după ce Elon Musk a deconectat armata rusă de la rețeaua Starlink. Află mai multe detalii citind articolul complet.""",
            "category": "Extern",
            "url": "https://www.digi24.ro/stiri/externe/ce-s-a-intamplat-dupa-ce-elon-musk-a-deconectat-armata-rusa-de-la-reteaua-starlink-3648433"
        },
        {
            "title": "AnalizăCât de realiste și eficiente sunt măsurile pentru relansarea economiei adoptate de Guvern. Ec",
            "content": """AnalizăCât de realiste și eficiente sunt măsurile pentru relansarea economiei adoptate de Guvern. Economist: Este o culegere de măsuri tehnice. Află mai multe detalii citind articolul complet.""",
            "category": "Economie",
            "url": "https://www.digi24.ro/stiri/economie/cat-de-realiste-si-eficiente-sunt-masurile-pentru-relansarea-economiei-adoptate-de-guvern-economist-este-o-culegere-de-masuri-tehnice-3647853"
        },
        {
            "title": "ExclusivAvertismentul consilierului lui Mugur Isărescu: Cum devin pensiile speciale o problemă socia",
            "content": """ExclusivAvertismentul consilierului lui Mugur Isărescu: Cum devin pensiile speciale o problemă socială. Află mai multe detalii citind articolul complet.""",
            "category": "Economie",
            "url": "https://www.digi24.ro/stiri/economie/avertismentul-consilierului-lui-mugur-isarescu-cum-devin-pensiile-speciale-o-problema-sociala-3648407"
        },
        {
            "title": "Peste 2.500 de hectare de pădure din Covasna au revenit în proprietatea statului. Decizia instanței ",
            "content": """Peste 2.500 de hectare de pădure din Covasna au revenit în proprietatea statului. Decizia instanței este definitivă. Află mai multe detalii citind articolul complet.""",
            "category": "Economie",
            "url": "https://www.digi24.ro/stiri/sci-tech/natura-si-mediu/peste-2-500-de-hectare-de-padure-din-covasna-au-revenit-in-proprietatea-statului-decizia-instantei-este-definitiva-3648145"
        },
        {
            "title": "Carnea de porc congelată nu va mai putea fi vândută ca proaspătă în România. Anunțul ministrului Flo",
            "content": """Carnea de porc congelată nu va mai putea fi vândută ca proaspătă în România. Anunțul ministrului Florin Barbu. Află mai multe detalii citind articolul complet.""",
            "category": "Economie",
            "url": "https://www.digi24.ro/stiri/economie/agricultura/carnea-de-porc-congelata-nu-va-mai-putea-fi-vanduta-ca-proaspata-in-romania-anuntul-ministrului-florin-barbu-3648097"
        },
        {
            "title": "Titularizare 2026: Calendarul complet al etapelor. Când au loc înscrierile și proba scrisă",
            "content": """Titularizare 2026: Calendarul complet al etapelor. Când au loc înscrierile și proba scrisă. Află mai multe detalii citind articolul complet.""",
            "category": "Educație",
            "url": "https://www.digi24.ro/stiri/actualitate/educatie/titularizare-2026-calendarul-complet-al-etapelor-cand-au-loc-inscrierile-si-proba-scrisa-3647859"
        },
        {
            "title": "Video„Şcoală săracă – Ţară needucată”: sindicaliștii din educație și studenții, protest la Cotroceni",
            "content": """Video„Şcoală săracă – Ţară needucată”: sindicaliștii din educație și studenții, protest la Cotroceni. Scrisoare deschisă pentru Nicușor Dan. Află mai multe detalii citind articolul complet.""",
            "category": "Educație",
            "url": "https://www.digi24.ro/stiri/actualitate/educatie/scoala-saraca-tara-needucata-protest-al-sidicalistilor-din-educatie-la-palatul-cotroceni-de-la-1200-la-1330-3647091"
        },
        {
            "title": "Video ExclusivUn fost consilier prezidențial și-a rupt diploma de doctor, în direct, la Digi24. „Dip",
            "content": """Video ExclusivUn fost consilier prezidențial și-a rupt diploma de doctor, în direct, la Digi24. „Diplomele de doctorat au ajuns o povară”. Află mai multe detalii citind articolul complet.""",
            "category": "Educație",
            "url": "https://www.digi24.ro/stiri/actualitate/un-fost-consilier-prezidential-si-a-rupt-diploma-de-doctor-in-direct-la-digi24-diplomele-de-doctorat-au-ajuns-o-povara-3644761"
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

# Disclaimer
st.markdown("""
<div style='text-align:center; color:gray; font-size:0.8em; margin-top:30px; padding:15px; background:rgba(255,255,255,0.05); border-radius:10px;'>
<b>⚠️ Disclaimer</b><br>
AziNews este un agregator de știri publice. Nu deținem conținutul afișat. <br>
Toate știrile aparțin surselor originale (Digi24). <br>
Acest serviciu este doar în scop informativ.
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align:center; color:gray;'>🤖 GarconAI - Asistentul tău personal</p>", unsafe_allow_html=True)
