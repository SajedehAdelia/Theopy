import speech_recognition as sr

r = sr.Recognizer()

def record_text():
    while True:
        try:
            with sr.Microphone(device_index=1) as source:
                print("Listening...")
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source)
                text = r.recognize_google(audio)
                return text

        except sr.UnknownValueError:
            print("Could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results: {e}")
        except Exception as e:
            print(f"Error: {e}")

while True:
    text = record_text()
    if text:
        print(f"You said: {text}")
