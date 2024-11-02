#!/usr/bin/python3.8
# -*- coding: utf-8 -*-

import datetime as dt
import os
import time

import telebot
from common import (
    compression_data,
    generate_report_for_re,
    get_mnemo_galagoliya,
    mnemo_garibjan,
    next_play,
    not_learn_word,
    parse_file,
    play_sound,
    read_file,
    send_message_from_bot,
    send_report,
    sound,
)
from config_bot import (
    name_base,
    path_file_not_learn,
    path_file_words,
    path_last_word,
    token,
    wait_sound,
)
from db import clear_table, create_base


def create_file_for_last_word(path_file: str) -> None:
    if not os.path.isfile(path_file):
        with open(path_file, mode="w", encoding="utf-8") as f:
            f.write("")


def write_last_file(path_file: str, word: str) -> None:
    with open(path_file, mode="w", encoding="utf-8") as f:
        f.write(word)


def prepate_data() -> None:
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
current_day = dt.date.today()

create_base(name_base)


@bot.message_handler(commands=["start"], content_types=["text"])
def test_fun(message) -> None:
    global current_day

    while True:
        for word_i in data_all_words[start_index : last_index + 1]:
            next_play()

            if word_i in words_not_learn:
                continue

            data_word = parse_file(word_i)
            send_message_from_bot(data_word[0])
            compression_data(name_base, data_word)

            if (dt.date.today() - current_day).days > 0:
                send_report(bot, "words_of_day")
                current_day = dt.date.today()
                clear_table(name_base, "words_of_day")
            if os.name == "nt":
                play_sound(word_i)
            else:
                sound(word_i)

            if not data_word[3]:
                write_last_file(path_last_word, word_i)
            time.sleep(wait_sound)
        else:
            prepate_data()


@bot.message_handler(content_types=["text"])
def get_text_messages(message) -> None:
    print("command: %s" % message.text)
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
            word_i = message.text.replace("_d", "")
            not_learn_word(word_i)
        elif message.text.endswith("_m"):
            word_i = message.text.replace("_m", "")
            garibjan = mnemo_garibjan.get(word_i, "")
            galagoliya = get_mnemo_galagoliya(word_i)
            send_message_from_bot(garibjan + "\n" + galagoliya)
        elif message.text.endswith("_r"):
            send_report(bot, "words_of_day")
        elif message.text.endswith("_re"):
            word_i = message.text.replace("_re", "")
            generate_report_for_re(bot, word_i)
        else:
            bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
    except Exception as e:
        print(e)


while True:
    try:
        # bot.polling(none_stop=True, interval=0)
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(e)
        time.sleep(10)
        # bot = telebot.TeleBot(token)
        current_day = dt.date.today()
        # bot.polling(none_stop=True, interval=0)
        raise
