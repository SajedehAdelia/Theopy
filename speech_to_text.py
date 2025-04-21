import speech_recognition as sr

r = sr.Recognizer()

print("Available microphones:")
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"{index}: {name}")

def record_text():
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"Microphone {index}: {name}")

    try:
        with sr.Microphone(device_index=3) as source:
            while True:
                print("Listening...")
                r.adjust_for_ambient_noise(source, duration=0.5)
                print("Ambient noice adjusted")
                audio = r.listen(source)
                print("Audio chunk recorded")
                text = r.recognize_google(audio)
                print(f"Recorded text: {text}")

    except sr.UnknownValueError:
        print("Could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results: {e}")
    except Exception as e:
        print(f"Error: {e}")

record_text()
