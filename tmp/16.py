import time
import speech_recognition as sr
import threading
import multiprocessing
import queue
from datetime import datetime
import pyttsx3


# ======== TTS в отдельном процессе (НЕ зависает) ========
def tts_process_main(q: multiprocessing.Queue):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('rate', 150)

    if voices:
        engine.setProperty('voice', voices[0].id)

    while True:
        text = q.get()
        if text is None:
            break

        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"[TTS-process] Ошибка синтеза: {e}")


class Voice:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_listening = False

        # процессы для TTS
        self.tts_queue = multiprocessing.Queue()
        self.tts_process = multiprocessing.Process(target=tts_process_main, args=(self.tts_queue,))
        self.tts_process.start()

        self.listening_thread = None

    # ----------- безопасный speak -----------
    def speak(self, text):
        print(f"[speak] {text}")
        self.tts_queue.put(text)

    def stop(self):
        print("[stop] Остановка...")
        self.is_listening = False
        self.tts_queue.put(None)
        self.tts_process.join(timeout=3)
        print("[stop] TTS остановлен")

    # ----------- микрофон -----------
    def calibrate_microphone(self):
        print("Калибровка микрофона...")
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Калибровка завершена!")
            return True
        except Exception as e:
            print(f"Ошибка калибровки микрофона: {e}")
            return False

    def listen(self):
        try:
            with self.microphone as source:
                print("Слушаю...")
                audio = self.recognizer.listen(source, timeout=7, phrase_time_limit=8)

            print("Распознаю речь...")
            text = self.recognizer.recognize_google(audio, language='ru-RU')
            print("Распознано:", text)
            return text.lower()

        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            print("Речь не распознана")
            return ""
        except Exception as e:
            print(f"Ошибка слушания: {e}")
            return ""

    # ----------- команды -----------
    def process_command(self, command):
        if not command:
            return

        print("Команда:", command)

        if "привет" in command:
            self.speak("Привет! Чем могу помочь?")
        elif "время" in command:
            now = datetime.now().strftime("%H:%M")
            self.speak(f"Сейчас {now}")
        elif "пока" in command or "стоп" in command:
            self.speak("До свидания")
            self.is_listening = False
        else:
            self.speak("Я пока не умею обрабатывать эту команду")

    # ----------- основной цикл -----------
    def listening_loop(self):
        print("Цикл прослушивания запущен")
        self.speak("Ассистент запущен. Слушаю команды")

        while self.is_listening:
            command = self.listen()
            if command:
                self.process_command(command)
            time.sleep(0.1)

    def start_listening(self):
        if not self.calibrate_microphone():
            self.speak("Ошибка микрофона")
            return

        self.is_listening = True
        self.listening_thread = threading.Thread(target=self.listening_loop)
        self.listening_thread.daemon = True
        self.listening_thread.start()


if __name__ == "__main__":
    v = Voice()

    try:
        v.start_listening()
        while v.is_listening:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Остановка пользователем")
    finally:
        v.stop()
        print("Ассистент завершил работу")
