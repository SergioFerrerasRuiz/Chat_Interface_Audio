import os
import requests
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env (opcional)
load_dotenv()

# Obtén la clave API desde las variables de entorno
api_key = os.getenv("GROQ_API_KEY")

# Verifica si la clave API está configurada
if not api_key:
    raise ValueError("La clave API no está configurada. Asegúrate de definir GROQ_API_KEY en el entorno.")

# URL de la API de Groq para generar resúmenes
url = "https://api.groq.com/openai/v1/chat/completions"

def generar_resumen(texto, lenguaje):

    data = {
    "model": "llama-3.3-70b-versatile",
    "messages": [
        {
            "role": "system",
            "content": (
                "Eres un asistente experto en resúmenes. Debes generar resúmenes precisos, claros y detallados, "
                "resaltando los puntos clave y datos importantes. Evita redundancias y responde en el idioma solicitado."
                "Se recibiran transcripciones de audio y es posible que haya que interpretar algunas palabras que no se definan correctamente, si esto ocurre buscaras una coherencia teniendo en cuenta el contenido previo del audio, si no hay similitud informaras de los errores encontrados. "
            )
        },
        {
            "role": "user",
            "content": (
                f"Resume el texto resaltando los puntos clave y detalles específicos, "
                f"Si se detecta el contexto de como se ha realizado el auido quiero que lo expecifiques tambien "
                f"evitando información irrelevante, en primer lugar, devolveras el texto sin cambios despues resumiras el texto y por ultimo me daras una lista de tags del texto. Responde en {lenguaje}: {texto}"
            )
        }
        
    ]
    , "temperature": 1,            # Controla creatividad (más preciso)
    #"max_tokens": 500,            # Mayor tamaño del resumen
    #"top_p": 0.9,                 # Balance entre creatividad y precisión
    #"frequency_penalty": 0.5,     # Reduce repeticiones
    #"presence_penalty": 0.5       # Fomenta diversidad
}

    # Cabeceras con la clave API
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    # Enviar la solicitud POST con el texto
    try:
        response = requests.post(url, headers=headers, json=data)

        # Manejo de la respuesta
        if response.status_code == 200:
            # Resumen exitoso
            print("Resumen generado correctamente")
            return response.json().get("choices")[0].get("message").get("content")
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"Error al generar el resumen: {e}")
        return None
