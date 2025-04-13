from flask import Flask, render_template, Response
import cv2
import pickle
import os
import face_recognition
import numpy as np

app = Flask(__name__)

# Create data directory if it doesn't exist
if not os.path.exists('data/'):
    os.makedirs('data/')

# Load existing face data if available
if 'faces_data.pkl' in os.listdir('data/'):
    with open('data/faces_data.pkl', 'rb') as f:
        known_faces = pickle.load(f)
    with open('data/names.pkl', 'rb') as f:
        known_names = pickle.load(f)
else:
    known_faces = []
    known_names = []

# Initialize video capture and face detection
video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def generate_frames():
    global known_faces, known_names

    while True:
        ret, frame = video.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = facedetect.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            crop_img = frame[y:y + h, x:x + w]
            resized_img = cv2.resize(crop_img, (150, 150))
            rgb_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)

            # Encode the face
            face_encoding = face_recognition.face_encodings(rgb_img)

            if face_encoding:
                face_encoding = face_encoding[0]
                matches = face_recognition.compare_faces(known_faces, face_encoding)
                name = "New User"

                if True in matches:
                    matched_idx = matches.index(True)
                    name = known_names[matched_idx]
                else:
                    name = "New User"
                    known_faces.append(face_encoding)
                    known_names.append(name)

                    # Save updated data
                    with open('data/faces_data.pkl', 'wb') as f:
                        pickle.dump(known_faces, f)
                    with open('data/names.pkl', 'wb') as f:
                        pickle.dump(known_names, f)

                cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (50, 50, 255), 2)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)

        # Convert frame to byte array and yield it
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
