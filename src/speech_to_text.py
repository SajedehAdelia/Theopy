import speech_recognition as sr

r = sr.Recognizer()


print("Available microphones:")
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"{index}: {name}")

import os

def record_text():
    mics = sr.Microphone.list_microphone_names()
    for index, name in enumerate(mics):
        print(f"Microphone {index}: {name}")

    if not mics:
        print("No microphones found. Ensure audio device is passed to Docker container.")
        # In a real MCP server, we might want to wait or exit gracefully.
        # For now, we'll exit to avoid the crash below.
        return


    mic_index_env = os.environ.get("MIC_INDEX")
    
    if mic_index_env:
        try:
            device_index = int(mic_index_env)
        except ValueError:
            print(f"Invalid MIC_INDEX: {mic_index_env}. Using default.")
            device_index = None
    else:
        device_index = None 
        print("No MIC_INDEX set, using default microphone.")

    try:
        # device_index=None uses the default microphone
        with sr.Microphone(device_index=device_index) as source:
            print(f"Using microphone index: {device_index if device_index is not None else 'Default'}")
            while True:
                print("Listening...")
                r.adjust_for_ambient_noise(source, duration=0.5)
                print("Ambient noice adjusted")
                audio = r.listen(source)
                print("Audio chunk recorded")
                try:
                    text = r.recognize_google(audio)
                    print(f"Recorded text: {text}")
                except sr.UnknownValueError:
                    print("Could not understand the audio.")
                except sr.RequestError as e:
                    print(f"Could not request results: {e}")
                    
    except OSError as e:
        print(f"Could not open microphone: {e}")
        print("If running in Docker, make sure to pass --device /dev/snd (Linux) or setup PulseAudio (Mac).")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    record_text()
