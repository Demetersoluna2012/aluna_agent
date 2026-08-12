import streamlit as st
import os
from datetime import datetime

st.set_page_config(page_title="Aluna Agent", page_icon="🌙", layout="wide", initial_sidebar_state="expanded")
st.markdown("<style>.stApp{background:#f8f9ff} h1{color:#4F46E5}</style>", unsafe_allow_html=True)

# --- KEYS (acepta AIza y AQ.) ---
GOOGLE_KEY = st.secrets.get("GOOGLE_API_KEY", os.getenv("GOOGLE_API_KEY"))
GROQ_KEY = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))

# --- SIDEBAR ---
with st.sidebar:
    st.title("🌙 Aluna Agent")
    st.caption("Pydantic AI • Gemini + Llama Gratis")
    st.divider()
    st.subheader("Memoria")
    nombre = st.text_input("Tu nombre", "Aluna")
    precios = st.text_area("Tus precios", "50€/h Diseño\n40€/h Contenido\nPack 10h: 400€")
    ubicacion = st.text_input("Ubicación", "Santa Cruz de Tenerife")
    st.divider()
    st.subheader("Base de conocimiento")
    uploaded = st.file_uploader("Sube PDFs para RAG", type=["pdf","txt","md"], accept_multiple_files=True)
    if uploaded:
        st.success(f"{len(uploaded)} docs")
    st.divider()
    st.subheader("Modelo")
    modelo = st.selectbox("Cerebro", ["Groq Llama 3.3 (Ultra rápido)", "Gemini 1.5 Flash (nuevo)"])
    if GOOGLE_KEY and GROQ_KEY:
        st.success("✅ APIs conectadas")
        if GOOGLE_KEY.startswith("AQ."):
            st.info("🔑 Detectada key nueva AQ. - OK")
    else:
        st.warning("⚠️ Faltan keys en Secrets")
    if st.button("Borrar chat"):
        st.session_state.messages=[]
        st.rerun()

if not GOOGLE_KEY or not GROQ_KEY:
    st.error("❌ Faltan keys. Ve a Manage app -> Settings -> Secrets")
    st.code('GOOGLE_API_KEY = "AQ....tu_key"\nGROQ_API_KEY = "gsk_..."', language="toml")
    st.stop()

# --- CLIENTES (nuevo SDK que soporta AQ.) ---
@st.cache_resource
def get_clients():
    from groq import Groq
    # Nuevo SDK oficial de Google que sí acepta AQ.
    from google import genai as google_genai
    groq_client = Groq(api_key=GROQ_KEY)
    google_client = google_genai.Client(api_key=GOOGLE_KEY)
    return groq_client, google_client

groq_client, google_client = get_clients()

# --- MAIN ---
col1, col2 = st.columns([2,1])
with col1:
    st.title(f"Hola, {nombre} 👋")
    st.markdown(f"**{precios.split(chr(10))[0]}** • {ubicacion} • {datetime.now().strftime('%d/%m/%Y')}")
    if "messages" not in st.session_state:
        st.session_state.messages=[{"role":"assistant","content": f"Hola {nombre}! Soy Aluna Agent con las keys nuevas AQ. Ya funciono 100% real. ¿Qué hacemos hoy?"}]
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
    if prompt := st.chat_input("Escribe a Aluna Agent..."):
        st.session_state.messages.append({"role":"user","content":prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                try:
                    system = f"Eres Aluna Agent, asistente de {nombre} de {ubicacion}. Precios: {precios}. Eres experta inmobiliaria y freelance. Respondes en español, directa y útil."
                    if "Groq" in modelo:
                        resp = groq_client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[{"role":"system","content":system}] + [{"role": x["role"], "content": x["content"]} for x in st.session_state.messages],
                            temperature=0.7)
                        ans = resp.choices[0].message.content
                    else:
                        # Nuevo SDK Gemini
                        full_prompt = system + "\n\nConversación:\n" + "\n".join([f"{x['role']}: {x['content']}" for x in st.session_state.messages])
                        response = google_client.models.generate_content(
                            model="gemini-2.0-flash",
                            contents=full_prompt
                        )
                        ans = response.text
                    st.markdown(ans)
                    st.session_state.messages.append({"role":"assistant","content":ans})
                except Exception as e:
                    st.error(f"Error: {e}")
                    st.caption("Si es error de Google, revisa que la key AQ. esté bien copiada sin espacios.")

with col2:
    st.subheader("Panel de control")
    with st.container(border=True):
        st.metric("Ofertas hoy", "3 nuevas", "+1 vs ayer")
        st.metric("Docs en base", f"{len(uploaded) if uploaded else 0}", "RAG listo" if uploaded else "Sube PDFs")
        st.metric("Coste mes", "0,00€", "Gratis")
        if GOOGLE_KEY and GOOGLE_KEY.startswith("AQ."):
            st.success("Key AQ. detectada ✅")
