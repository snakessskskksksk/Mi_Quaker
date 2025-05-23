from flask import Flask, request, redirect, url_for, send_from_directory, render_template
import os

app = Flask(__name__)

# Configuración de la carpeta de subida
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No se encontró ningún archivo", 400
    file = request.files['file']
    if file.filename == '':
        return "No se seleccionó ningún archivo", 400
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return f"Archivo subido exitosamente: {file.filename}"

if __name__ == '__main__':
    app.run(debug=True)