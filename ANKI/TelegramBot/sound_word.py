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
from common import sound, parse_file, play_sound
from config_bot import count_sound, path_dir_mp3, path_to_mplayer, time_sound_pause, path_dir, path_last_word, path_file_words, wait_sound


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

create_file_for_last_word(path_last_word)
data_all_words = read_file(path_file_words)
last_word_session = read_file(path_last_word)

start_index = 0
last_index = len(data_all_words) - 1

if last_word_session:
    start_index = data_all_words.index(last_word_session[0])
    if start_index == last_index:
        start_index = 0


while True:
    for ind, word_i in enumerate(data_all_words[start_index: last_index]):
        parse_file(word_i)
        
        # path_file_open = os.path.join(path_dir_for_notepad, name_file)
        # info_word = get_first_line(path_file_open)# .encode("utf-8").decode("cp866")
        # print(str(ind) + "   " + info_word)
        
        # sound(word_i)
        play_sound(word_i)

        write_last_file(path_last_word, word_i)
        time.sleep(wait_sound)
    else:
        start_index = 0
        command = input("Для завершения введите q или enter чтобы продлолжить:\n")
        print("#" * 50)
        if command == "q":
            sys.exit()


