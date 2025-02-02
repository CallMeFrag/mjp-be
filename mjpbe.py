from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import json

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Il backend è online e funziona!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# Configurazione cartelle per caricamento file
UPLOAD_FOLDER = './uploads'
EXPORT_FOLDER = './exports'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXPORT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Simulazione del database per i gioielli
jewelry_database = {
    "earrings": [],
    "nose_rings": [],
    "belly_rings": []
}

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Salvataggio file
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Associazione al database
    jewelry_type = request.form.get("type")
    if jewelry_type not in jewelry_database:
        return jsonify({"error": "Invalid jewelry type"}), 400

    jewelry_database[jewelry_type].append({
        "filename": filename,
        "path": file_path
    })

    return jsonify({"message": "File uploaded successfully", "type": jewelry_type}), 200

@app.route('/jewelry', methods=['GET'])
def get_jewelry():
    return jsonify(jewelry_database), 200

@app.route('/export', methods=['POST'])
def export_3d_model():
    data = request.get_json()
    jewelry_type = data.get("type")
    if jewelry_type not in jewelry_database:
        return jsonify({"error": "Invalid jewelry type"}), 400

    models = jewelry_database[jewelry_type]
    export_path = os.path.join(EXPORT_FOLDER, f"{jewelry_type}_models.json")

    with open(export_path, 'w') as export_file:
        json.dump(models, export_file)

    return jsonify({"message": f"3D models exported successfully to {export_path}"}), 200

if __name__ == '__main__':
    app.run(debug=True)
