import requests
from googletrans import Translator

def get_city():
    translator = Translator()
    response = requests.get('https://ipinfo.io')
    data = response.json()
    return data.get('city')
