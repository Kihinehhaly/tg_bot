from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import telebot
from django.conf import settings
from telegram_bot.bot_main import bot
# Create your views here.


@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        json_str = request.body.decode('utf-8')
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_update([update])
    return HttpResponse()


def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=settings.WEBHOOK_URL + 'telegram_webhook')
