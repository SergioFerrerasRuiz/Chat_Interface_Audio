import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from modules.groq_client import apicall  # Método para preguntas en texto
from modules.transcriptor import transcribir_audio  # Método para transcribir
from modules.resumidor import generar_resumen  # Método para resumir

# Configuración de Flask
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__,
            template_folder=os.path.join(BASE_DIR, "templates"),
            static_folder=os.path.join(BASE_DIR, "static"))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

chat_history = []  # Historial de mensajes

@app.route('/')
def home():
    return render_template("chat.html")

@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.json.get('question')
    if not user_question:
        return jsonify({'error': 'No question provided'}), 400

    answer = apicall(user_question)
    chat_history.append({'user_question': user_question, 'answer': answer})
    
    return jsonify({'answer': answer})

@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No se envió archivo'}), 400

    file = request.files['audio']
    if file.filename == '':
        return jsonify({'error': 'Archivo vacío'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Transcribir el audio
    transcripcion = transcribir_audio(filepath, "es")
    if not transcripcion:
        return jsonify({'error': 'Error al transcribir'}), 500

    # Generar resumen
    resumen = generar_resumen(transcripcion, "es")
    if not resumen:
        return jsonify({'error': 'Error al resumir'}), 500

    return jsonify({
        'filename': filename,
        'transcription': transcripcion,
        'summary': resumen
    })


if __name__ == "__main__":
    app.run(debug=False)
