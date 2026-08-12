import streamlit as st
from dataclasses import dataclass
import os
from datetime import datetime

# CONFIG
st.set_page_config(
    page_title="Aluna Agent",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded"
)

@dataclass
class AlunaData:
    nombre: str = "Aluna"
    rol: str = "Freelance"
    precios: str = "50€/h - Diseño, 40€/h - Contenido"
    ubicacion: str = "Tenerife"

# --- SIDEBAR - TU MEMORIA ---
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
        st.success(f"{len(uploaded)} docs cargados")
        for f in uploaded:
            st.caption(f"• {f.name}")
    
    st.divider()
    st.subheader("Modelo")
    modelo = st.selectbox("Modelo gratis", ["google-gla:gemini-2.0-flash", "groq:llama-3.3-70b-versatile"])
    
    st.divider()
    st.info("💡 Todo corre 100% gratis con keys de AI Studio y Groq")

# --- MAIN ---
col1, col2 = st.columns([2, 1])

with col1:
    st.title(f"Hola, {nombre} 👋")
    st.markdown(f"**{precios.split(chr(10))[0]}** • {ubicacion} • {datetime.now().strftime('%d/%m/%Y')}")

    # CHAT
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": f"Hola {nombre}! Soy Aluna Agent. Puedo buscar ofertas, resumir tu base de conocimiento y hacer recados. ¿Qué hacemos hoy?"}
        ]

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if prompt := st.chat_input("Escribe a Aluna Agent..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Aquí iría la llamada real a tu Pydantic Agent
        # from pydantic_ai import Agent ... agent.run_sync(prompt)
        # Por ahora respuesta de demo que muestra la arquitectura
        with st.chat_message("assistant"):
            # Simulación de cómo respondería con RAG + Tools
            if "oferta" in prompt.lower() or "malt" in prompt.lower():
                response = f"""
**Buscando ofertas para ti, {nombre}...** (tool: `buscar_web`)

Encontré 3 que encajan con {precios}:

1.  **Diseño de marca para startup** - 600€ - Malt (verificada)
2.  **Redacción 10 artículos SEO** - 400€ - Upwork
3.  **Dashboard Streamlit** - 750€ - Cliente directo

¿Quieres que genere las propuestas? (tool: `genera_propuesta` con validación Pydantic)
                """
            elif "base" in prompt.lower() or "pdf" in prompt.lower():
                response = f"Tengo {len(uploaded) if uploaded else 0} docs en tu base. Si me preguntas algo, haré RAG: busco en tus PDFs con embeddings de Gemini (gratis) y respondo citando la fuente. Sube algo en la izquierda para probar."
            else:
                response = f"""
Entendido: *"{prompt}"*

Así lo haría tu agente real con Pydantic AI:

1.  **Memoria**: Sé que eres {nombre} de {ubicacion} con precios {precios}
2.  **RAG**: Busco en tu base ({len(uploaded) if uploaded else 0} docs)
3.  **Tool**: Si hace falta, llamo a API (web, email, etc.)
4.  **Validación**: Pydantic valida que la respuesta tenga formato correcto antes de mostrarla

Esto ahora es demo visual. Para activarlo 100% real, añade tus 2 keys en el código (línea 70).
                """
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

with col2:
    st.subheader("Panel de control")
    
    with st.container(border=True):
        st.metric("Ofertas hoy", "3 nuevas", "+1 vs ayer")
        st.metric("Docs en base", f"{len(uploaded) if uploaded else 0}", "RAG listo" if uploaded else "Sube PDFs")
        st.metric("Coste mes", "0,00€", "Gemini + Groq gratis")
    
    with st.container(border=True):
        st.write("**Próximos pasos para hacerlo 100% real:**")
        st.markdown("""
        1.  Pon tus keys en `st.secrets`
        2.  Descomenta el bloque `Agent` (línea 70)
        3.  Deploy a Hugging Face Spaces (gratis)
        
        Te queda URL tipo: `aluna-agent.hf.space`
        """)
        st.code("pip install pydantic-ai chromadb streamlit duckduckgo-search python-dotenv", language="bash")

    st.caption("Hecho por Aluna con Pydantic AI • 100% tuyo")
