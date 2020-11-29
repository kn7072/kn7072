# -*- coding: utf-8 -*-
import config_bot
import telebot
from common import sound, parse_file

bot = telebot.TeleBot(config_bot.token)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.endswith("_s"):
        word_i = message.text.replace("_s", "")
        print(word_i)
        sound(word_i)
        # bot.send_message(message.from_user.id, word_i)
    elif message.text.endswith("_e"):
        word_i = message.text.replace("_e", "")
        parse_file(word_i, send_examples=True)
        # bot.send_message(message.from_user.id, "Напиши привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

bot.polling(none_stop=True, interval=0)    

