# Aluna Agent 🏠

Asistente inmobiliario con IA usando Gemini + Groq.

## Deploy gratis en Streamlit Cloud

1. Haz fork de este repo
2. Ve a https://share.streamlit.io/
3. New app -> selecciona este repo
4. En Advanced Settings -> Secrets añade:

```
GOOGLE_API_KEY = "tu_key_AIza"
GROQ_API_KEY = "tu_key_gsk"
```

5. Deploy

## Local

```
pip install -r requirements.txt
streamlit run app.py
```

Creado con ❤️
