import json
import wave
import os
import sys
from vosk import Model, KaldiRecognizer


class OfflineSpeechRecognizer:
    def __init__(self, language="ru", model_name="vosk-model-small-ru-0.22"):
        self.language = language
        self.model_name = model_name
        self._model = None
        self.sample_rate = 16000  # Vosk требует 16kHz

    @property
    def model(self):
        """Ленивая загрузка модели - только при первом обращении"""
        if self._model is None:
            self._load_model()
        return self._model

    def _load_model(self):
        """Загрузка модели в память"""
        model_path = f"models/{self.model_name}"

        if not os.path.exists(model_path):
            print(f"Модель не найдена по пути: {model_path}")
            print("Пожалуйста, скачайте модель с: https://alphacephei.com/vosk/models")
            print("И распакуйте её в папку 'models'")
            return False

        try:
            print(f"Загрузка модели {self.model_name}...")
            self._model = Model(model_path)
            print(f"Модель для языка {self.language} успешно загружена")
            return True
        except Exception as e:
            print(f"Ошибка при загрузке модели: {e}")
            return False

    def recognize_from_microphone(self, duration=None, timeout=None, phrase_time_limit=None):
        """
        Распознавание речи с микрофона в реальном времени

        Параметры:
        - duration: максимальная длительность записи в секундах (если None, запись до тишины)
        - timeout: время ожидания начала речи в секундах
        - phrase_time_limit: максимальная длительность фразы
        """
        try:
            import pyaudio
            import time

            # Проверяем загрузку модели
            if not self.model:
                print("Модель не загружена")
                return ""

            # Инициализация PyAudio
            p = pyaudio.PyAudio()

            # Проверяем доступные устройства ввода
            default_input = p.get_default_input_device_info()
            print(f"Используется микрофон: {default_input['name']}")

            # Открываем поток с правильными параметрами
            stream = p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=4000,
                input_device_index=None  # Используем устройство по умолчанию
            )

            print("Слушаю... (говорите что-нибудь)")
            if duration:
                print(f"Длительность записи: {duration} секунд")
            print("Для остановки нажмите Ctrl+C")
            print("-" * 50)

            # Инициализация распознавателя Vosk
            rec = KaldiRecognizer(self.model, self.sample_rate)
            rec.SetWords(True)  # Включаем распознавание отдельных слов
            results = []
            silent_chunks = 0
            max_silent_chunks = 50  # ~2 секунды тишины для остановки (при 4000 фреймов)
            start_time = time.time()

            try:
                while True:
                    # Проверка на максимальную длительность
                    if duration and (time.time() - start_time) > duration:
                        print(f"\nДостигнута максимальная длительность записи ({duration} сек)")
                        break

                    # Читаем данные с микрофона
                    data = stream.read(4000, exception_on_overflow=False)

                    # Проверяем наличие звука (простое определение тишины)
                    if max(data) < 10:  # Порог тишины
                        silent_chunks += 1
                    else:
                        silent_chunks = 0

                    # Если долго тихо - завершаем запись
                    if silent_chunks > max_silent_chunks and len(results) > 0:
                        print("\nОбнаружена длительная тишина, завершение записи")
                        break

                    # Отправляем данные в распознаватель
                    if rec.AcceptWaveform(data):
                        # Получаем промежуточный результат
                        result = json.loads(rec.Result())
                        if result.get("text"):
                            results.append(result["text"])
                            print(f"Промежуточно: {result['text']}")
                    else:
                        # Показываем частичные результаты
                        partial = json.loads(rec.PartialResult())
                        if partial.get("partial"):
                            # Очищаем строку и выводим частичный результат
                            #sys.stdout.write('\r' + ' ' * 50 + '\r')
                            return partial['partial']
                            #sys.stdout.write(f"\rРаспознаю: {partial['partial']}")
                            #sys.stdout.flush()

            except KeyboardInterrupt:
                print("\n\nЗапись остановлена пользователем")

            print()  # Переход на новую строку

            # Получаем финальный результат
            final_result = json.loads(rec.FinalResult())
            if final_result.get("text"):
                results.append(final_result["text"])

            # Закрываем поток
            stream.stop_stream()
            stream.close()
            p.terminate()

            # Объединяем все результаты
            recognized_text = " ".join(results)

            if recognized_text:
                print(f"Распознано: {recognized_text}")
            else:
                print("Ничего не распознано")

            return recognized_text.strip()

        except ImportError:
            print("Библиотека PyAudio не установлена")
            print("Установите её: pip install pyaudio")
            print("Для Windows может потребоваться: pip install pipwin && pipwin install pyaudio")
            return ""

        except Exception as e:
            print(f"Ошибка при записи с микрофона: {e}")
            import traceback

            traceback.print_exc()
            return ""



'''recognizer = OfflineSpeechRecognizer(
    language="ru",
    model_name="vosk-model-small-ru-0.22"  # Используйте маленькую модель
)

text = recognizer.recognize_from_microphone()
print(text)
'''