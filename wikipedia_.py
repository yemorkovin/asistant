import wikipedia
import re

class Wiki:
    def __init__(self):
        wikipedia.set_lang('ru')
    def search(self, query):
        page = wikipedia.page(query)

        return {
            'title': page.title,
            'content': ' '.join(self.split_reg(page.content)[:5])
        }


    def split_reg(self, text):
        return re.split(r'(?<=[.!?])\s+(?=[A-ZА-Я])', text)

#w = Wiki()
#print(w.search('Популярный язык программирования'))

'''import wikipediaapi
import requests


class Wiki:
    def __init__(self):
        self.wikipedia = wikipediaapi.Wikipedia(
            language='ru',
            extract_format=wikipediaapi.ExtractFormat.WIKI,
            user_agent='MyProject/1.0 (admin@yemorkovin.ru)'
        )
    def search(self, query):
        ulr = f'https://ru.wikipedia.org/w/api.php'
        params = {
            'action': 'query',
            'format': 'json',
            'list': 'search',
            'srsearch': query,
            'srlimit': '1',
            'utf8': 1,
            'origin': '*'
        }
        response = requests.get(url=ulr, params=params)
        data = response.json()
        print(data)
    def search_(self, query):

        search_results = self.wikipedia.page(query)
        if not search_results.exists():
            print('Не найдено')
            return []
        w = search_results.text.split('.')
        print(w)


s = Wiki()
s.search_('Эссекс_(королевство)')

'''