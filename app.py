from flask import Flask, request, jsonify, render_template
import speech_recognition as sr
import os
from pydub import AudioSegment
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcrib_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file sent'}), 400
        
    audio_file = request.files['audio']
    filename = secure_filename(audio_file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    audio_file.save(filepath)
    
    # SpeechRecognition needs wav format
    wav_path = filepath.rsplit('.', 1)[0] + '.wav'
    audio = AudioSegment.from_file(filepath)
    audio.export(wav_path, format='wav')

    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        recorded_audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(recorded_audio)
        return jsonify({'text': text})
    except sr.UnknownValueError:
        return jsonify({'error': 'Could not understand audio'}), 400
    except sr.RequestError as e:
        return jsonify({'error': f'Request failed: {e}'}), 500


if __name__ == '__main__':
    app.run(debug=True)