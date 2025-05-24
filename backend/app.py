from flask import Flask, request, send_from_directory
import os

app = Flask(__name__)

# Configuración de la carpeta de subida
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    # Sirve el archivo index.html desde la carpeta frontend
    return send_from_directory('../frontend', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Maneja la subida de archivos
    if 'file' not in request.files:
        return "No se encontró ningún archivo", 400
    file = request.files['file']
    if file.filename == '':
        return "No se seleccionó ningún archivo", 400
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return f"Archivo subido exitosamente: {file.filename}"

@app.route('/list', methods=['GET'])
def list_files():
    # Lista los archivos subidos en la carpeta uploads
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    if not files:
        return "No hay currículos subidos."
    file_links = [f"<div class='file-item'><a href='/download/{file}'>{file}</a></div>" for file in files]
    return "\n".join(file_links)

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    # Permite descargar un archivo específico
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
    
@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        return f"Archivo {filename} eliminado exitosamente."
    return "Archivo no encontrado", 404