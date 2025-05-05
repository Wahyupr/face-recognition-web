from flask import Flask, request, jsonify, send_from_directory
import face_recognition
from PIL import Image
import numpy as np
import io

app = Flask(__name__, static_folder='static')

# Load known face
known_image = face_recognition.load_image_file("known_faces/person1.jpg")
known_encoding = face_recognition.face_encodings(known_image)[0]

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/recognize', methods=['POST'])
def recognize():
    file = request.files['image']
    img = face_recognition.load_image_file(file)
    encodings = face_recognition.face_encodings(img)
    
    if not encodings:
        return jsonify({"result": "No face found"})
    
    match = face_recognition.compare_faces([known_encoding], encodings[0])[0]
    return jsonify({"result": "Match" if match else "No match"})

if __name__ == '__main__':
    app.run(debug=True)
