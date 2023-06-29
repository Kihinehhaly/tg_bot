import telebot
from django.conf import settings
import os
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
        "X-RapidAPI-Key": settings.RAPID_TOKEN or "caa6de3ac1msh6470d51d49affa4p11a51djsnbce8a7e058d9",
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
        'appid': settings.WEATHER_TOKEN,
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


bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    template = make_template('start')
    username = message.chat.username
    msg = template.render(username=username)
    pin = bot.send_message(message.chat.id, text=msg, parse_mode='html')
    bot.pin_chat_message(message.chat.id, message_id=pin.id)


@bot.message_handler(commands=['help'])
def help(message):
    template = make_template('help')
    msg_text = template.render()
    bot.send_message(message.chat.id, text=msg_text, parse_mode='html')


@bot.message_handler(commands=['dog'])
def send_dog(message):
    img = get_dog_image()
    bot.send_photo(message.chat.id, photo=img)


@bot.message_handler(commands=['horo'])
def get_horo(message):
    signs = ['Aries ♈️', 'Taurus ♉️', 'Gemini ♊️', 'Cancer ♋️',
             'Leo ♌️', 'Virgo ♍️', 'Libra ♎️', 'Scorpio ♏️',
             'Sagittarius ♐️', 'Capricorn ♑️', 'Aquarius ♒️', 'Pisce ♓️']
    markup = telebot.types.ReplyKeyboardMarkup(row_width=3)
    buttons = [telebot.types.KeyboardButton(sign) for sign in signs]
    markup.add(*buttons)
    bot.send_message(message.chat.id, 'Выбери свой знак зодиака:', reply_markup=markup)


@bot.message_handler(commands=['contact', 'weather'])
def contact_info(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    cont_btn = telebot.types.KeyboardButton('Номер телефона', request_contact=True)
    loc_btn = telebot.types.KeyboardButton('Локация', request_location=True)
    markup.add(cont_btn)
    markup.add(loc_btn)
    bot.send_message(message.chat.id, 'Делись', reply_markup=markup)


@bot.message_handler(content_types=['contact', 'location'])
def user_info(message):
    if message.contact is not None:
        text = f'#contacts\nName: {message.contact.first_name}, Surname: {message.contact.last_name}, Phone: {message.contact.phone_number}'
        bot.send_message(1260306029, text)
        bot.send_message(message.chat.id, 'Спасибочки!', reply_markup=telebot.types.ReplyKeyboardRemove())
    elif message.location is not None:
        lat = {message.location.latitude}
        lon = {message.location.longitude}
        text = f'#location\nUser ID: {message.chat.id}, Location: {lat},{lon}'
        bot.send_message(1260306029, text)
        weather = get_weather(lat, lon)
        bot.send_message(message.chat.id, text=weather, parse_mode='html',
                         reply_markup=telebot.types.ReplyKeyboardRemove())


@bot.callback_query_handler(func=lambda call: call.data in ['low', 'medium', 'high'])
def handle_password_generate(call):
    complexity = call.data
    password = generate_password(complexity)
    bot.send_message(call.maessage.chat.id, 'Password: ')
    bot.send_message(call.message.chat.id, password, reply_markup=telebot.types.ReplyKeyboardRemove())


@bot.message_handler(commands=['password'])
def handle_password_send(message):
    bot.send_message(message.chat.id, 'Выбери сложность пароля: ',
                     reply_markup=generate_keyboard())


@bot.message_handler(content_types=['text'])
def zodiac(message):
    signs = ['Aries', 'Taurus', 'Gemini', 'Cancer',
             'Leo', 'Virgo', 'Libra', 'Scorpio',
             'Sagittarius', 'Capricorn', 'Aquarius', 'Pisce']
    if message.text[:-3] in signs:
        zodiac_sign = message.text[:-3]
        res = parse_horo(zodiac_sign.lower())
        template = make_template('zodiac')
        msg = template.render(forecast=res)
        bot.send_message(message.chat.id, text=msg, parse_mode='html', reply_markup=telebot.types.ReplyKeyboardRemove())


if __name__ == '__main__':
    bot.polling()

