import os
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("La clave API no está configurada. Asegúrate de definir GROQ_API_KEY en el entorno.")

url = "https://api.groq.com/openai/v1/chat/completions"

# Historial de la conversación
historial = [
    {"role": "system", "content": "Eres un chat genérico y gracioso, que responderá en el idioma detectado. Decorarás todas tus respuestas con algunos emojis como 😊 😄 😉 para que sean más bonitas, ademas añadiras espacios para que el texto sea mas legible y usaras mayusculas y al empezar a hablar. No uses markdown, pero sí añade emojis en tus respuestas."}
]

def apicall(texto):
    global historial  # Usamos la lista global para almacenar la memoria
    
    # Agregar el mensaje del usuario al historial
    historial.append({"role": "user", "content": texto})
    
    # Limitar el historial a los últimos 10 mensajes para evitar sobrecarga
    if len(historial) > 10:
        historial = [historial[0]] + historial[-9:]
    
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": historial,  # Se envía todo el historial
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
        respuesta = response_json.get("choices", [{}])[0].get("message", {}).get("content", "No response")
        
        # Agregar la respuesta del bot al historial
        historial.append({"role": "assistant", "content": respuesta})
        
        return respuesta
    except requests.exceptions.RequestException as e:
        return f"Error en la API: {str(e)}"
