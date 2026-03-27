import time
import speech_recognition as sr
import threading
from datetime import datetime

from Thread_ import Thread_
from commands.schedule_by_day import schedule_subject
from scan_disc import ProgramSearcher
from siler_audio import Silero_
from num2words import num2words
from query_request import Query
from dotenv import load_dotenv
from search_google import Search_google
import json
import models
from user_data.change_city import change_city, get_weather_link
from vosk_recognizer import get_text
from wikipedia_ import Wiki

audio_silero = Silero_()
qr = Query()

load_dotenv()


class Voice:
    def __init__(self):

        self.model_weather = models.Load_model.model_sentence_transformer
        self.q = Thread_()
        self.q.start()
        with open('data.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)['intents'].keys()
        self.ps = ProgramSearcher()
        self.is_listening = False
        self.listening_thread = None
        self.calibrate_microphone()
        self.google = Search_google()

    def speak(self, text):
        print(f"[speak] {text}")
        #audio_silero.silero_tts_basic(text)
        self.q.add(audio_silero.silero_tts_basic, text)
        #thread = threading.Thread(target=audio_silero.silero_tts_basic, args=(text,))
        #thread.start()

    def stop(self):
        print("[stop] Остановка...")
        self.is_listening = False

    def calibrate_microphone(self):
        print("Калибровка микрофона...")
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
            print("Калибровка завершена!")
            return True
        except Exception as e:
            print(f"Ошибка калибровки микрофона: {e}")
            return False

    def listen(self):
        try:
            text = get_text()
            print("Распознаю речь...")
            print(f"Распознано: {text}")
            return text.lower()

        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            print("Речь не распознана")
            return ""
        except Exception as e:
            print(f"Ошибка слушания: {e}")
            return ""

    def delete_command(self, command, indent):
        commands_words = command.split()
        for i in range(len(commands_words)):
            if qr.get_intent(commands_words[i]) == indent:

                command = command.replace(commands_words[i], '')
        command = command.strip()
        if command.startswith('в '):
            command = command[2:]
        return command

    def process_command(self, command):
        if not command:
            return
        index = command.find('барсик')
        if index != -1:
            command = command[index:]
        if not command.startswith('барсик'):
            return
        
        print(f"Команда: {command}")
        command = command.replace('барсик', '').strip()
        if qr.get_intent(command):
            self.q.clear()
        if qr.get_intent(command) == 'greeting':
            self.speak("Привет! Рад вас слышать!")
        elif qr.get_intent(command) == 'wikipedia':
            w = Wiki()
            c = w.search('Популярный язык программирования')
            self.speak(c['title'])
            self.speak(c['content'])
        elif qr.get_intent(command) == "search":
            '''commands_words = command.split()
            for i in range(len(commands_words)):
                if qr.get_intent(commands_words[i]) == 'search':
                    command = command.replace(commands_words[i], '')
            command = command.strip()
            if command.startswith('в '):
                command = command[2:]
            '''
            command = self.delete_command(command, 'search')

            ss = self.google.search(command)
            sss = []
            ss_d = ''
            for i, res in enumerate(ss, 1):
                if res.get('description') == '':
                    continue
                sss.append({
                    'title': res.get('title', 'Без заголовка'),
                    'link': res.get('url', ''),
                    'description': res.get('description', '')
                })
                ss_d += f'{res.get('title', 'Без заголовка')}. '
            ress = f'Найдено { num2words(len(sss), lang='ru')} страниц'
            ress += ss_d

            self.speak(ress)
        elif qr.get_intent(command) == 'time':
            h = datetime.now().strftime("%H")
            m = datetime.now().strftime("%M")
            a_h = num2words(h, lang='ru')
            a_m = num2words(m, lang='ru')
            self.speak(f"Сейчас {a_h} {a_m}")
        elif qr.get_intent(command) == 'weather':
            from commands.weather import get_weather
            from parser_weather import parser
            try:
                parser()
                w = get_weather(command, self.model_weather)
                self.speak(f"{w}")
            except:
                pass
        elif qr.get_intent(command) == 'farewell':
            self.speak("До свидания! Выключаюсь.")
            self.is_listening = False
        elif qr.get_intent(command) == 'schedule_by_day':
            schedule_subject(command, self.speak)
        elif qr.get_intent(command) == 'open_program':
            command = self.delete_command(command, 'open_program')
            self.speak(self.ps.search_s(command))
        elif qr.get_intent(command) == 'change_city':
            city = change_city(command)
            if city!= None:
                get_weather_link(city)
                self.speak(f'Город изменен на {city}')
            else:
                get_weather_link()
        else:
            self.speak("Пока не понимаю эту команду.")

    def listening_loop(self):
        print("Цикл прослушивания запущен")
        self.speak("Ассистент запущен. Говорите команды")


        while True:
            if self.is_listening:
                command = self.listen()

                if command and command.strip():
                    self.process_command(command)
                    time.sleep(0.5)
            else:
                command = self.listen()
                if command:
                    if command.lower().strip() == 'квант проснись':
                        self.is_listening = True

    def start_listening(self):
        if self.is_listening:
            print("Уже слушаем...")
            return
        self.is_listening = True
        self.listening_loop()
        print("Прослушивание запущено")


if __name__ == "__main__":
    v = Voice()
    try:
        v.start_listening()
        print("Ассистент активен. Нажмите Ctrl+C для остановки.")

        while v.is_listening:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nОстановка пользователем")
    finally:
        v.stop()
        print("Ассистент завершил работу")
