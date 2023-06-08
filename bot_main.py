import telebot
import stuff


bot = telebot.TeleBot('')


@bot.message_handler(commands=['start'])
def start(message):
    template = stuff.make_template('start')
    username = message.chat.username
    msg = template.render(username=username)
    pin = bot.send_message(message.chat.id, text=msg, parse_mode='html')
    bot.pin_chat_message(message.chat.id, message_id=pin.id)


@bot.message_handler(commands=['dog'])
def send_dog(message):
    img = stuff.get_dog_image()
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


@bot.message_handler(content_types=['text'])
def zodiac(message):
    signs = ['Aries', 'Taurus', 'Gemini', 'Cancer',
             'Leo', 'Virgo', 'Libra', 'Scorpio',
             'Sagittarius', 'Capricorn', 'Aquarius', 'Pisce']
    if message.text[:-3] in signs:
        zodiac_sign = message.text[:-3]
        res = stuff.parse_horo(zodiac_sign.lower())
        bot.send_message(message.chat.id, text=res)


if __name__ == '__main__':
    bot.polling()

