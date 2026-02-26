import streamlit as st
import requests
from datetime import datetime
import pytz

# Set timezone Romania
bucharest_tz = pytz.timezone('Europe/Bucharest')
now_bucharest = datetime.now(bucharest_tz)

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
st.markdown(f"<p style='text-align:center;'>{now_bucharest.strftime('%A, %d %B %Y')} | România</p>", unsafe_allow_html=True)
st.markdown("---")

# ============ INFO RAPIDE (SUS) ============
st.markdown("## 📊 Informații Rapide")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### ☀️ Vremea")
    try:
        r = requests.get("https://api.open-meteo.com/v1/forecast?latitude=44.43&longitude=26.10&current_weather=true", timeout=5)
        if r.status_code == 200:
            temp = r.json()['current_weather']['temperature']
            st.markdown(f"<p class='big-text'>{temp}°C</p>", unsafe_allow_html=True)
    except:
        st.markdown("<p class='big-text'>4°C</p>", unsafe_allow_html=True)
    st.markdown("București")
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🕐 Ora")
    st.markdown(f"<p class='big-text'>{now_bucharest.strftime('%H:%M')}</p>", unsafe_allow_html=True)
    st.markdown(now_bucharest.strftime('%A'))
    st.markdown("</div>", unsafe_allow_html=True)

with c3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 💱 Curs")
    try:
        r_eur = requests.get("https://api.frankfurter.app/latest?from=EUR&to=RON", timeout=5)
        r_usd = requests.get("https://api.frankfurter.app/latest?from=USD&to=RON", timeout=5)
        eur = r_eur.json().get("rates", {}).get("RON", "N/A")
        usd = r_usd.json().get("rates", {}).get("RON", "N/A")
        st.markdown(f"<p class='big-text'>€ {eur}</p>", unsafe_allow_html=True)
        st.markdown(f"$ {usd}" if usd != "N/A" else "$ -")
    except:
        st.markdown(f"<p class='big-text'>€ 5.10</p>", unsafe_allow_html=True)
        st.markdown("$ 4.60")
    st.markdown("RON")
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
            "title": "Șoferii cu permis emis în străinătate ar putea primi documentul înapoi doar după ce achită amenda, î",
            "content": """Șoferii care au permisul de conducere eliberat de o autoritate străină și cărora li s-a suspendat dreptul de a conduce în România ar putea fi obligați să își achite integral amenda înainte de a-și rec""",
            "category": "Economie",
            "url": "https://www.digi24.ro/stiri/economie/soferii-cu-permis-emis-in-strainatate-ar-putea-primi-documentul-inapoi-doar-dupa-ce-achita-amenda-inainte-de-a-parasi-romania-3649043"
        },
        {
            "title": "Amplu caz de proxenetism într-un club de striptease din Capitală. Zeci de victime obligate să întreț",
            "content": """Procurorii Direcției de Investigare a Infracțiunilor de Criminalitate Organizată și Terorirsm (DIICOT) fac joi, 26 februarie, percheziții într-un amplu dosar care vizează o grupare care a exploatat ze""",
            "category": "Actualitate",
            "url": "https://www.digi24.ro/stiri/actualitate/justitie/amplu-caz-de-proxenetism-intr-un-club-de-striptease-din-capitala-zeci-de-victime-obligate-sa-intretina-relatii-sexuale-cu-clientii-3649063"
        },
        {
            "title": "O imagine cu greutate: Kim Jong-un și fiica lui, „desemnată ca succesoare”, au apărut asortați în ha",
            "content": """Fiica adolescentă a lui Kim Jong-un, Ju-ae, a apărut alături de tatăl său, în fotografiile de stat publicate pentru a marca etapele finale ale congresului Partidului Muncitorilor, aflat la guvernare î""",
            "category": "Extern",
            "url": "https://www.digi24.ro/stiri/externe/coreea-de-nord/o-imagine-cu-greutate-kim-jong-un-si-fiica-lui-desemnata-ca-succesoare-au-aparut-asortati-in-haine-de-piele-la-o-parada-militara-3649067"
        },
        {
            "title": "Accident surprins pe camera de bord: bărbat cu ordin de protecție, reținut după ce a lovit mașina fo",
            "content": """Un bărbat de 27 de ani din Caraș-Severin a fost reținut după ce a lovit în trafic mașina fostei sale partenere, deși avea emis pe numele său un ordin de protecție și era monitorizat prin brățară elect""",
            "category": "Actualitate",
            "url": "https://www.digi24.ro/stiri/actualitate/evenimente/accident-surprins-pe-camera-de-bord-barbat-cu-ordin-de-protectie-retinut-dupa-ce-a-lovit-masina-fostei-partenere-3649093"
        },
        {
            "title": "Bogdan Ivan, după vizita la Washington: Obiectivul e clar - investiţii în infrastructură strategică,",
            "content": """Ministrul Energiei, Bogdan Ivan, afirmă că a discutat, în cadrul unei vizite făcute la Washington, despre obţinerea de mai multă energie în bandă pentru România, investiţii de miliarde în infrastructu""",
            "category": "Actualitate",
            "url": "https://www.digi24.ro/stiri/actualitate/bogdan-ivan-dupa-vizita-la-washington-obiectivul-e-clar-investitii-in-infrastructura-strategica-proiecte-nucleare-duse-la-capat-3649045"
        },
        {
            "title": "Criză de pământuri rare în SUA: industria aerospațială și semiconductorii, afectați de blocajele Chi",
            "content": """Deficitul de pământuri rare esențiale pentru industria aerospațială și producția de cipuri din Statele Unite se adâncește, în pofida armistițiului comercial dintre Washington și Beijing, iar unele com""",
            "category": "Extern",
            "url": "https://www.digi24.ro/stiri/externe/criza-de-pamanturi-rare-in-sua-industria-aerospatiala-si-semiconductorii-afectati-de-blocajele-chinei-reuters-3648883"
        },
        {
            "title": "Din 6 martie, Jurnalul de Științe revine la Digi World",
            "content": """Din 6 martie, Jurnalul de Științe revine la Digi World Citește mai mult pe Digi24.""",
            "category": "Actualitate",
            "url": "https://www.digi24.ro/stiri/actualitate/din-6-martie-jurnalul-de-stiinte-revine-la-digi-world-3649033"
        },
        {
            "title": "„Un bolnav cu mintea tulburată”. Donald Trump a răbufnit după ce Robert De Niro i-a îndemnat pe amer",
            "content": """Actorul Robert De Niro este „un bolnav cu mintea tulburată”, a afirmat miercuri preşedintele american pe reţeaua sa Truth Social, după ce actorul a făcut un apel la „alungarea” administraţiei Trump pe""",
            "category": "Extern",
            "url": "https://www.digi24.ro/stiri/externe/sua/un-bolnav-cu-mintea-tulburata-donald-trump-a-rabufnit-dupa-ce-robert-de-niro-i-a-indemnat-pe-americani-sa-i-reziste-presedintelui-3648983"
        },
        {
            "title": "Alertă de gripă aviară în Cluj: două lebede, găsite moarte în zona unui lac de acumulare. Au fost st",
            "content": """Alertă de gripa aviară în Cluj, după ce două lebede au fost găsite moarte în zona unui lac de acumulare. Autoritățile au stabilit zone de restricție pentru a opri răspândirea bolii și oamenii sunt obl""",
            "category": "Actualitate",
            "url": "https://www.digi24.ro/stiri/actualitate/alerta-de-gripa-aviara-in-cluj-doua-lebede-gasite-moarte-in-zona-unui-lac-de-acumulare-au-fost-stabilite-mai-multe-restrictii-3648993"
        },
        {
            "title": "Rusia încearcă „să se joace” cu Donald Trump pentru a amâna negocierile de pace, spune Volodimir Zel",
            "content": """În cadrul unui interviu acordat la Kiev pentru televiziunea Fox News, apropiată lui Donald Trump, Volodimir Zelenski a afirmat că Rusia încearcă „să se joace cu preşedintele Statelor Unite” şi să trag""",
            "category": "Extern",
            "url": "https://www.digi24.ro/stiri/externe/ue/rusia-incearca-sa-se-joace-cu-donald-trump-pentru-a-amana-negocierile-de-pace-spune-volodimir-zelenski-nu-poate-sa-ne-ocupe-3648999"
        },
        {
            "title": "Permis suspendat pentru neplata amenzilor. Cseke Attila: „Va aduce o colectare mult mai bună”. Ce tr",
            "content": """Schimbarea legii privind neplata amenzilor de circulație înseamnă suspendarea permisului de șofer în cazul rău-platnicilor. Perioada de suspendare este calculată în funcție de valoarea amenzii. Pentru""",
            "category": "Economie",
            "url": "https://www.digi24.ro/stiri/economie/permis-suspendat-pentru-neplata-amenzilor-ce-trebuie-sa-stie-soferii-cseke-attila-va-aduce-o-colectare-mult-mai-buna-3648945"
        },
        {
            "title": "Ședința CGMB de joi, suspendată din cauza absenței consilierilor PSD, PUSL și AUR. Ce proiecte erau ",
            "content": """Consilierii generali ai Capitalei au fost convocați în şedinţă joi, de la ora 10:00, pentru a dezbate o serie de proiecte, printre care unele privind desfiinţarea Centrului Expo Arte şi creşterea chir""",
            "category": "Actualitate",
            "url": "https://www.digi24.ro/stiri/noua-sedinta-la-cgmb-in-contextul-tensiunilor-dintre-primarul-general-ciprian-ciucu-si-consilierii-psd-ce-proiecte-sunt-pe-agenda-3648775"
        },
        {
            "title": "Donald Trump a venit cu un nou termen în care vrea să pună capăt războiului din Ucraina",
            "content": """Președintele SUA, Donald Trump, a declarat în timpul unei convorbiri telefonice cu liderul ucrainean Volodimir Zelenski că dorește să pună capăt războiului din Ucraina cât mai curând posibil, au infor""",
            "category": "Extern",
            "url": "https://www.digi24.ro/stiri/externe/sua/donald-trump-a-venit-cu-un-nou-termen-in-care-vrea-sa-puna-capat-razboiului-din-ucraina-3648941"
        },
        {
            "title": "Rusia acuză SUA de „provocare agresivă” după incidentul din largul coastelor Cubei: „Să declanşeze u",
            "content": """Maria Zaharova, purtătoarea de cuvânt a Ministerului rus al Afacerilor Externe, a acuzat Statele Unite de „provocare agresivă” după incidentul petrecut în largul coastelor Cubei cu nava înregistrată î""",
            "category": "Extern",
            "url": "https://www.digi24.ro/stiri/externe/rusia/rusia-acuza-sua-de-provocare-agresiva-dupa-incidentul-din-largul-coastelor-cubei-sa-declanseze-un-conflict-3648939"
        },
        {
            "title": "FBI concediază agenți implicați în ancheta documentelor clasificate păstrate de Trump la Mar-a-Lago",
            "content": """FBI a concediat cel puţin şase agenţi implicaţi într-o anchetă din 2022 privind reţinerea de către Donald Trump a unor documente clasificate la reşedinţa sa din Mar-a-Lago, a relatat miercuri The Guar""",
            "category": "Extern",
            "url": "https://www.digi24.ro/stiri/externe/sua/fbi-concediaza-agenti-implicati-in-ancheta-documentelor-clasificate-pastrate-de-trump-la-mar-a-lago-3648911"
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
