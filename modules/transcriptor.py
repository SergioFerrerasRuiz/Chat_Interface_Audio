import os
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("La clave API no está configurada. Asegúrate de definir GROQ_API_KEY en el entorno.")

# URL de la API de Groq para transcripciones
url = "https://api.groq.com/openai/v1/audio/transcriptions"

def transcribir_audio(audio_path, lenguaje="es"):
    """
    Función para transcribir un archivo de audio utilizando la API de Groq.

    :param audio_path: Ruta del archivo de audio.
    :param lenguaje: Idioma del audio (por ejemplo, "es" para español).
    :return: El texto transcrito si la solicitud es exitosa, o None si ocurre un error.
    """
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    try:
        with open(audio_path, "rb") as audio_file:
            files = {
                "file": audio_file
            }
            data = {
                "model": "whisper-large-v3",  # Modelo de transcripción
                "language": lenguaje
            }

            response = requests.post(url, headers=headers, files=files, data=data)

        if response.status_code == 200:
            return response.json().get("text")
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"Error al procesar el archivo de audio: {e}")
        return None
