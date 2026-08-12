import streamlit as st
import os
from groq import Groq
import google.generativeai as genai

st.set_page_config(page_title="Aluna Agent", page_icon="🏠", layout="wide")

# --- CONFIG ---
st.markdown("""
<style>
.stApp { background: #f8f9ff; }
h1 { color: #4F46E5; }
</style>
""", unsafe_allow_html=True)

st.title("🏠 Aluna Agent - Tu asistente inmobiliario con IA")
st.caption("Conectado a Gemini + Groq - Gratis y rápido")

# Cargar keys
GOOGLE_KEY = st.secrets.get("GOOGLE_API_KEY", os.getenv("GOOGLE_API_KEY"))
GROQ_KEY = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))

if not GOOGLE_KEY or not GROQ_KEY:
    st.error("❌ Faltan las API Keys en Secrets. Ve a Settings -> Secrets y añade GOOGLE_API_KEY y GROQ_API_KEY")
    st.stop()

# Inicializar clientes
@st.cache_resource
def get_clients():
    genai.configure(api_key=GOOGLE_KEY)
    groq_client = Groq(api_key=GROQ_KEY)
    return groq_client

groq_client = get_clients()
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Configuración")
    modelo = st.selectbox("Elige cerebro:", ["Groq Llama 3.3 (Ultra rápido)", "Gemini 1.5 Flash (Google)"])
    st.divider()
    st.success("✅ APIs conectadas")
    if st.button("Borrar chat"):
        st.session_state.messages = []
        st.rerun()

# --- CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "¡Hola! Soy Aluna Agent 🏠 ¿En qué te ayudo hoy con tu piso?"}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Escribe aquí...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                if "Groq" in modelo:
                    response = groq_client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "system", "content": "Eres Aluna Agent, un asistente experto inmobiliario amable, directo y que ayuda a vender/alquilar pisos. Respondes en español."}] + 
                                 [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                        temperature=0.7
                    )
                    answer = response.choices[0].message.content
                else:
                    # Gemini
                    chat = gemini_model.start_chat(history=[])
                    # reconstruir historial simple
                    full_prompt = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
                    resp = gemini_model.generate_content(full_prompt)
                    answer = resp.text

                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Error: {e}")
