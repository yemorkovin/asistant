from datetime import datetime
from num2words import num2words

from schedule.parser_csv_json import get_schedule


def schedule(command, speak):
    d = {
        'понедельник': 'пн',
        'вторник': 'вт',
        'среда': 'ср',
        'четверг': 'чт',
        'пятница': 'пт',
    }
    day = None
    for day_of_week, sr_day_of_week in d.items():
        if day_of_week.lower() in command.lower():
            day = sr_day_of_week
    if day:
        schedule = get_schedule(day)
        for index_n, data_schedule in schedule.items():
            time = data_schedule[0].split(':')
            speak(f'Расписание на время {num2words(time[0], lang='ru')} {num2words(time[1], lang='ru')}')
            speak(f'Предмет: {data_schedule[1]}')
        if schedule:
            pass
        else:
            pass
    else:
        if 'сегодня' in command:
            now = datetime.now()
            day_today = now.weekday()
            schedule = None
            if day_today <= 4:
                day_ = list(d.items())[day_today]
                schedule = day_
            if schedule:
                schedule = get_schedule(schedule[1])
                for index_n, data_schedule in schedule.items():
                    time = data_schedule[0].split(':')
                    speak(f'Расписание на время {num2words(time[0], lang='ru')} {num2words(time[1], lang='ru')}')
                    speak(f'Предмет: {data_schedule[1]}')
            else:
                speak(f'Рассписаний на сегодня не найдено')
        elif 'завтра' in command:
            now = datetime.now()
            day_today = now.weekday() + 1
            schedule = None
            if day_today <= 4:
                day_ = list(d.items())[day_today]
                schedule = day_
            if schedule:
                schedule = get_schedule(schedule[1])
                for index_n, data_schedule in schedule.items():
                    time = data_schedule[0].split(':')
                    speak(f'Расписание на время {num2words(time[0], lang='ru')} {num2words(time[1], lang='ru')}')
                    speak(f'Предмет: {data_schedule[1]}')
            else:
                speak(f'Рассписаний на сегодня не найдено')



#schedule('Рассписание сегодня', '')