import telebot
from jinja2 import Template


bot = telebot.TeleBot('')


@bot.message_handler(commands=['start'])
def start(message):
    with open('templates/start.html', 'r', encoding='utf-8') as f:
        text = f.read()
    ans = Template(text)
    bot.send_message(message.chat.id, ans.render(username=message.chat.username), parse_mode='html')


if __name__ == '__main__':
    bot.polling()



