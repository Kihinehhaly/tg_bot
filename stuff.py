import requests as r
from jinja2 import Template


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
    return res['general'][0]