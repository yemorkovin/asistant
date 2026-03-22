import locale

from dotenv import load_dotenv
from sentence_transformers import util
import pandas as pd
from datetime import datetime, timedelta
import models
from num2words import num2words
from pymorphy3 import MorphAnalyzer
morph = MorphAnalyzer()
load_dotenv()

def get_res_f(query, model, m):
    program_embs = model.encode(m, convert_to_tensor=True)
    a = query.split()
    total_res = []
    for w in a:
        query_em = model.encode(w, convert_to_tensor=True)

        s = util.cos_sim(query_em, program_embs)[0]
        res = []
        for idx, i in enumerate(s):
            if i.item() >= 0.9:
                res.append({
                    'index': idx,
                    'k': i.item(),
                    'name': m[idx]
                })
        res = sorted(res, key=lambda a: a['k'], reverse=True)
        if res:
            total_res.append(res[0])
    return total_res


def get_date_by_weekday(target_weekday):
    weekdays = {
        "понедельник": 1,
        "вторник": 2,
        "среда": 3,
        "четверг": 4,
        "пятница": 5,
        "суббота": 6,
        "воскресенье": 7
    }
    target_weekday = weekdays[target_weekday]

    today = datetime.now()
    current_weekday = today.isoweekday()
    days_diff = target_weekday - current_weekday

    if days_diff <= 0:
        days_diff += 7

    target_date = today + timedelta(days=days_diff)
    months = ["янв", "фев", "мар", "апр", "май", "июн", "июл", "авг", "сен", "окт", "ноя", "дек"]
    return f'{target_date.day} {months[target_date.month - 1]}'



def get_weather(query, model=None):
    data_weather = pd.read_csv('weather_data.csv')
    model = models.Load_model.model_sentence_transformer
    day_of_week = ['сегодня', 'завтра']
    res = get_res_f(query, model, day_of_week)
    res = sorted(res, key=lambda a: a['k'], reverse=True)
    f = None
    if res:
        f = res[0]['name']
    locale.setlocale(locale.LC_TIME, 'russian')
    now = datetime.now()
    if f == 'сегодня':
        day_of_month = now.day
        month_short = now.strftime("%b")
        key = f'{day_of_month} {month_short}'
        today = data_weather[data_weather['date'] == key]
        temp = morph.parse('градус')[0]

        return (f'Сегодня погода в Коробово. Минимальная температура {num2words(today.iloc[0]['temp_min'], lang='ru')} градуса. '
                f'Максимальная температура {num2words(today.iloc[0]['temp_max'] ,lang='ru') }  {temp.make_agree_with_number(today.iloc[0]['temp_max']).word}. '
                f'{today.iloc[0]['description']}')
    elif f == 'завтра':
        next_day = now + timedelta(days=1)
        day_of_month = next_day.day
        month_short = next_day.strftime("%b")
        key = f'{day_of_month} {month_short}'
        today = data_weather[data_weather['date'] == key]

        return (
            f'Погода на завтра в Коробово. Минимальная температура {num2words(today.iloc[0]['temp_min'], lang='ru')} градуса. '
            f'Максимальная температура {num2words(today.iloc[0]['temp_max'], lang='ru')} градуса. '
            f'{today.iloc[0]['description']}')

    else:
        m = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]
        res = get_res_f(query, model, m)
        if res:
            key = get_date_by_weekday(res[0]['name'])
            today = data_weather[data_weather['date'] == key]
            t = res[0]['name']
            if res[0]['name'] == 'среда':
                t = 'среду'
            elif res[0]['name'] == 'суббота':
                t = 'субботу'
            elif res[0]['name'] == 'пятница':
                t = 'пятницу'

            return (
                f'Погода на {t} в Коробово. Минимальная температура {num2words(today.iloc[0]['temp_min'], lang='ru')} градуса. '
                f'Максимальная температура {num2words(today.iloc[0]['temp_max'], lang='ru')} градуса. '
                f'{today.iloc[0]['description']}')
        else:
            data_weather = pd.read_csv('weather_data_now.csv')
            return (
                f'Погода сейчас в Коробово. Температура {num2words(data_weather.iloc[0]['now_weather'], lang='ru')} градуса. '
                f'Ощущается как {num2words(data_weather.iloc[0]['now_feel'], lang='ru')} градуса. '
                f'{data_weather.iloc[0]['now_desc']}')



#print(get_weather('Погода'))