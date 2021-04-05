# -*- coding: utf-8 -*-
from config_bot import token, path_file_not_learn
import telebot
import os
from common import sound, parse_file, play_sound, prepare_garibjan, send_message_from_bot, prepare_galagoliya

bot = telebot.TeleBot(token)
mnemo_garibjan = prepare_garibjan()
mnemo_galagoliya = prepare_galagoliya()


def get_mnemo_galagoliya(word):
    list_temp = []
    delimetr = "#"*30
    result = ""
    for i in mnemo_galagoliya:
        block_i = "\n".join(i)
        if word in block_i:
            list_temp.append(block_i)

    if list_temp:
        result = delimetr.join(list_temp)
    return result    


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    try:
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
            garibjan = mnemo_garibjan.get(word_i, "")
            galagoliya = get_mnemo_galagoliya(word_i)
            
            send_message_from_bot(garibjan + "\n" + galagoliya)

        else:
            bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
    except Exception as e:
        print(e)        


bot.polling(none_stop=True, interval=0)    

