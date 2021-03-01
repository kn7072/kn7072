# -*- coding: utf-8 -*-
from config_bot import token, path_file_not_learn
import telebot
import os
from common import sound, parse_file, play_sound, prepare_garibjan, send_message_from_bot

bot = telebot.TeleBot(token)
mnemo_garibjan = prepare_garibjan()


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.endswith("_s"):
        word_i = message.text.replace("_s", "")
        print(word_i)
        if os.name == "nt":
            play_sound(word_i)
        else:
            sound(word_i)
        # bot.send_message(message.from_user.id, word_i)
    elif message.text.endswith("_e"):
        word_i = message.text.replace("_e", "")
        parse_file(word_i, send_examples=True)
        # bot.send_message(message.from_user.id, "Напиши привет")
    elif message.text.endswith("_d"):
        with open(path_file_not_learn, encoding="utf-8", mode="a") as f:
            word_i = message.text.replace("_d", "")
            f.write(word_i + "\n")
    elif message.text.endswith("_m"):
        word_i = message.text.replace("_m", "")
        garibjan = mnemo_garibjan.get(word_i, "-")
        send_message_from_bot(garibjan)

    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


bot.polling(none_stop=True, interval=0)    

