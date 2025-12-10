from pyowm import OWM

API_KEY = '6113571abf7c8bf78caf9d3e58b648b0'
own = OWM(API_KEY)
mgr = own.weather_manager()

obs = mgr.weather_at_place('Москва,RU')
weather = obs.weather
res = f'Теипература: {weather.temperature('celsius')['temp']} Влажность: {weather.humidity}%'
print(res)