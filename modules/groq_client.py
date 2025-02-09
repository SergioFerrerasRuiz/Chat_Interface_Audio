import os
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("La clave API no está configurada. Asegúrate de definir GROQ_API_KEY en el entorno.")

url = "https://api.groq.com/openai/v1/chat/completions"

def apicall(texto):
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "Eres un chat genérico que responderá en el idioma detectado. Decorarás todas tus respuestas con algunos emojis como 😊 😄 😉 para que sean más bonitas. No uses markdown, pero sí añade emojis en tus respuestas."},
            {"role": "user", "content": texto}
        ],
        "temperature": 1
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()
        return response_json.get("choices", [{}])[0].get("message", {}).get("content", "No response")
    except requests.exceptions.RequestException as e:
        return f"Error en la API: {str(e)}"
