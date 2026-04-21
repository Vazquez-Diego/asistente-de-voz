import pyttsx3
from datetime import datetime
import ollama
import vosk
import json
import pyaudio

# =========================
# VOZ OFFLINE (ARREGLADA)
# =========================
def speak(text):
    print(f"IA: {text}")

    # reiniciar engine cada vez (evita que se trabe)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')

    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 180)
    engine.setProperty('volume', 1.0)

    engine.say(text)
    engine.runAndWait()


# =========================
# VOSK (OFFLINE)
# =========================
model = vosk.Model(r"C:\Users\Diego Vazquez\Downloads\vosk-model-small-es-0.42\vosk-model-small-es-0.42")

mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16,
                  channels=1,
                  rate=16000,
                  input=True,
                  frames_per_buffer=8192)

stream.start_stream()

recognizer = vosk.KaldiRecognizer(model, 16000)


def listen():
    print("Asistente: escuchando...")

    while True:
        data = stream.read(4096, exception_on_overflow=False)

        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "")

            if text:
                print(f"Tú: {text}")
                return text.lower()


# =========================
# IA LOCAL
# =========================
chat_history = []

def preguntar_ia(texto):
    global chat_history

    try:
        chat_history.append({"role": "user", "content": texto})

        response = ollama.chat(
            model="llama3.2:3b",
            messages=chat_history
        )

        respuesta = response['message']['content']
        chat_history.append({"role": "assistant", "content": respuesta})

        return respuesta

    except Exception as e:
        print("Error IA:", e)
        return "Tuve un problema con la inteligencia artificial."


# =========================
# MAIN
# =========================
def main():
    speak("Hola, soy tu asistente sin internet")

    while True:
        command = listen()

        if not command:
            continue

        if "salir" in command:
            speak("Adiós")
            break

        elif "hora" in command:
            hora = datetime.now().strftime("%H:%M")
            speak(f"La hora es {hora}")

        elif "nombre" in command:
            speak("Soy tu asistente inteligente")

        else:
            respuesta = preguntar_ia(command)
            speak(respuesta)


# =========================
# INICIO
# =========================
if __name__ == "__main__":
    main()