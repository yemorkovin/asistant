import pyaudio
import json
from vosk import Model, KaldiRecognizer
from dotenv import load_dotenv
import os

def get_text():
    load_dotenv()

    # Загружаем модель
    model = Model(os.getenv('VOSK_MODEL'))

    # Частота 16000 обязательна для большинства моделей
    recognizer = KaldiRecognizer(model, 16000)

    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=8000)

    stream.start_stream()


    try:
        while True:
            data = stream.read(4000, exception_on_overflow=False)

            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                return result.get("text")
            else:
                partial = json.loads(recognizer.PartialResult())


    except KeyboardInterrupt:
        print("\nОстановлено")

    stream.stop_stream()
    stream.close()
    p.terminate()


