import requests as r
from jinja2 import Template
import datetime as dt
import random
import string
import json


def get_dog_image():
    url = 'https://random.dog/woof.json'
    resp = r.get(url).json()
    return resp['url']


def make_template(filename):
    with open(f'templates/{filename}.html', 'r', encoding='utf-8') as f:
        text = f.read()
    template = Template(text)
    return template


def parse_horo(sign):
    url = f"https://horoscopes-ai.p.rapidapi.com/get_horoscope_en/{sign}/tomorrow/general"

    headers = {
        "X-RapidAPI-Key": "caa6de3ac1msh6470d51d49affa4p11a51djsnbce8a7e058d9",
        "X-RapidAPI-Host": "horoscopes-ai.p.rapidapi.com"
    }
    response = r.get(url, headers=headers)
    res = response.json()
    try:
        return res['general'][0]
    except:
        return 'У владельца бота закончились запросы к API'


def get_weather(lat, lon):
    url = 'https://api.openweathermap.org/data/2.5/forecast'
    params = {
        'appid': '',
        'lat': lat,
        'lon': lon,
        'units': 'metric',
        'lang': 'ru',
    }
    response = r.get(url, params=params).json()
    text = '<strong>{}</strong>:\n{}°С {}\n\n'
    resp = ''
    try:
        for data in response['list']:
            date = dt.datetime.fromtimestamp(data['dt'])
            date_res = date.strftime('%d.%m.%Y | %H.%M')
            temp = data['main']['temp']
            weather = data['weather'][0]['description']

            if date.hour == 6 or date.hour == 18:
                resp += text.format(date_res, temp, weather)
        return resp
    except:
        print('Something wrong here')


def generate_password(complexity):
    length = 8
    characters = string.ascii_lowercase + string.digits
    if complexity == 'medium':
        length = 12
        characters += string.ascii_uppercase
    elif complexity == 'high':
        length = 16
        characters +=string.ascii_uppercase + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def generate_keyboard():
    kb = {
        'inline_keyboard': [
            [{'text': 'Низкая', 'callback_data': 'low'}],
            [{'text': 'Средняя', 'callback_data': 'medium'}],
            [{'text': 'Высокая', 'callback_data': 'high'}],
        ]
    }
    kb_json = json.dumps(kb)
    return kb_json
