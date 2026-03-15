import json
import wave
import os
from vosk import Model, KaldiRecognizer


class OfflineSpeechRecognizer:

    def __init__(self, language="ru"):

        self.language = language
        self.model = None
        self.load_model()

    def load_model(self):
        model_path = f"models/vosk-model-ru-0.10"

        if not os.path.exists(model_path):
            print(f"Модель не найдена по пути: {model_path}")
            print("Пожалуйста, скачайте модель с: https://alphacephei.com/vosk/models")
            print("И распакуйте её в папку 'models'")
            return False

        try:
            self.model = Model(model_path)
            print(f"Модель для языка {self.language} успешно загружена")
            return True
        except Exception as e:
            print(f"Ошибка при загрузке модели: {e}")
            return False

    def recognize_from_microphone(self, duration=5):
        try:
            import pyaudio

            if not self.model:
                print("Модель не загружена")
                return ""

            p = pyaudio.PyAudio()
            stream = p.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=16000,
                            input=True,
                            frames_per_buffer=4000)

            print(f"Слушаю... (длительность: {duration} секунд)")

            rec = KaldiRecognizer(self.model, 16000)
            rec.SetWords(True)

            results = []
            frames = []

            for _ in range(0, int(16000 / 4000 * duration)):
                data = stream.read(4000)
                frames.append(data)

                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    if "text" in result:
                        results.append(result["text"])

            final_result = json.loads(rec.FinalResult())
            if "text" in final_result:
                results.append(final_result["text"])

            stream.stop_stream()
            stream.close()
            p.terminate()

            recognized_text = " ".join(results)

            print(f"Распознано: {recognized_text}")
            return recognized_text.strip()

        except ImportError:
            print("Библиотека PyAudio не установлена")
            print("Установите её: pip install pyaudio")
            return ""
        except Exception as e:
            print(f"Ошибка при записи с микрофона: {e}")
            return ""



recognizer = OfflineSpeechRecognizer(language="ru")

text = recognizer.recognize_from_microphone(duration=5)
print(f"С микрофона распознано: {text}")

