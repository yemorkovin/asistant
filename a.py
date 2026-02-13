import  json
import os

r = [
    {
        '13:00':
            {
                'id': 1,
                'title': 'математика',
                'кабинет': 102,
                'учитель': 'Петров'
            },
        '14:00':
            {
                'id': 2,
                'title': 'физика',
                'кабинет': 103,
                'учитель': 'Иванова'
            },
        '15:00':
            {
                'id': 3,
                'title': 'физра',
                'кабинет': 103,
                'учитель': 'Иванова'
            },
        '16:00':
            {
                'id': 4,
                'title': 'география',
                'кабинет': 103,
                'учитель': 'Иванова'
            },
    }
]

#with open('Понедельник.json', 'w', encoding='utf-8') as f:
#    json.dump(r, f, indent=4)


command = 'Какое понедельник расписание'

day_of_week = os.listdir('schedule')
name_file = None
for j in command.split():
    j = j.lower()
    for i in day_of_week:
        q = i.replace('.json', '').lower()
        if j == q:
            name_file = i
            break

with open(f'schedule/{name_file}') as f:
    r = json.load(f)
for time, data in r[0].items():
    print(time)
    print(data)

