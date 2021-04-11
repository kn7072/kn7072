# -*- coding: utf-8 -*-

import sys
from subprocess import Popen, PIPE
import os
import signal
import time
import re
import telebot
import requests
import config_bot
from common import sound, parse_file, play_sound, next_play, prepare_garibjan, send_message_from_bot, prepare_galagoliya, get_data_file
from config_bot import count_sound, path_dir_mp3, path_to_mplayer, time_sound_pause, path_dir, \
    path_last_word, path_file_words, wait_sound, path_file_not_learn, token
from datetime import datetime, timedelta
import datetime as dt


def create_file_for_last_word(path_file):
    if not os.path.isfile(path_file):
        with open(path_file, mode="w", encoding="utf-8") as f:
            f.write("")


def read_file(path_file):
    list_word = []
    for i in open(path_file, mode="r", encoding="utf-8"):
        list_word.append(i.split(";")[0].strip())
    return list_word


def write_last_file(path_file, word):
    with open(path_file, mode="w", encoding="utf-8") as f:
        f.write(word)


def prepate_data():
    global data_all_words
    global words_not_learn
    global start_index
    global last_index

    create_file_for_last_word(path_last_word)
    data_all_words = read_file(path_file_words)
    words_not_learn = read_file(path_file_not_learn)
    last_word_session = read_file(path_last_word)

    start_index = 0
    last_index = len(data_all_words) - 1
    assert last_index > 0, "Нет слов для изучения"

    if last_word_session:
        start_index = data_all_words.index(last_word_session[0])
        if start_index == last_index:
            start_index = 0

prepate_data()

bot = telebot.TeleBot(token)
mnemo_garibjan = prepare_garibjan()
mnemo_galagoliya = prepare_galagoliya()
words_of_day = []
current_day = dt.date.today() 


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


@bot.message_handler(commands=["start"], content_types=['text'])
def test_fun(message):
    global current_day
    # for i in range(10):
    #     bot.send_message(message.from_user.id, "Я ")
    #     time.sleep(5)
    while True:
        for ind, word_i in enumerate(data_all_words[start_index: last_index]):
            
            print(f"DEBUG {word_i}")

            next_play()

            
            if word_i in words_not_learn:
                continue
            data_word = parse_file(word_i)
            send_message_from_bot(data_word[0])
            words_of_day.append(data_word)
            if (dt.date.today() - current_day).days > 0:
                words_of_day.clear()
                current_day = dt.date.today()
            
            # path_file_open = os.path.join(path_dir_for_notepad, name_file)
            # info_word = get_first_line(path_file_open)# .encode("utf-8").decode("cp866")
            # print(str(ind) + "   " + info_word)

            if os.name == "nt":
                play_sound(word_i)
            else:
                sound(word_i)

            write_last_file(path_last_word, word_i)
            time.sleep(wait_sound)
        else:
            prepate_data()
            # start_index = 0
            # command = input("Для завершения введите q или enter чтобы продлолжить:\n")
            # print("#" * 50)
            # if command == "q":
            #     sys.exit()


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
            data_word = parse_file(word_i)  # , send_examples=True
            send_message_from_bot("\n".join(data_word[2]))
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
        elif message.text.endswith("_r"):
            all_messages = []
            temp_html = get_data_file("test.html")
            for first_line, mnemo, examples in words_of_day:
                word_i, transcription, translate = [i.strip() for i in first_line.split("|")]
                word_transcription = f"{word_i} |{transcription}|"
                if not mnemo:
                    garibjan = mnemo_garibjan.get(word_i, "")
                    galagoliya = get_mnemo_galagoliya(word_i)
                    mnemo = garibjan + "\n" + galagoliya
                    mnemo_text = mnemo.replace("\xa0", "")
                    mnemo = [i for i in mnemo_text.split("\n") if i]

                mnemo_html = "\n".join([f"<div>{i}</div>" for i in mnemo])
                examples_html = "\n".join([f"<div>{i}</div>" for i in examples])
                word_html = config_bot.temp_html.format(word=word_transcription, translate=translate, mnemo=mnemo_html, examples=examples_html)
                all_messages.append(word_html)
            all_messages_text = "\n".join(all_messages)
            # html_report = temp_html.format(html_words=all_messages_text) 
            html_report = temp_html % (all_messages_text)
            html_report = html_report.encode("utf-8")
            with open("report.html", mode="wb+") as f:
                f.write(html_report)
                f.seek(0)
                bot.send_document(message.from_user.id, f)   

        else:
            bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
    except Exception as e:
        print(e)        

print()
bot.polling(none_stop=True, interval=0) 


# while True:
    
#     for ind, word_i in enumerate(data_all_words[start_index: last_index]):
#         next_play()
#         if word_i in words_not_learn:
#             continue
#         data_word = parse_file(word_i)
#         words_of_day.append(data_word)
#         if (dt.date.today() - current_day).days > 0:
#             words_of_day.clear()
        
#         # path_file_open = os.path.join(path_dir_for_notepad, name_file)
#         # info_word = get_first_line(path_file_open)# .encode("utf-8").decode("cp866")
#         # print(str(ind) + "   " + info_word)

#         if os.name == "nt":
#             play_sound(word_i)
#         else:
#             sound(word_i)

#         write_last_file(path_last_word, word_i)
#         time.sleep(wait_sound)
#     else:
#         prepate_data()
#         # start_index = 0
#         # command = input("Для завершения введите q или enter чтобы продлолжить:\n")
#         # print("#" * 50)
#         # if command == "q":
#         #     sys.exit()


