# -*- coding: utf-8 -*-

import sys
from subprocess import Popen, PIPE
import os
import signal
import time
import re

pattern_mnemo = "{{(?P<mnemo>.+?)}}"
pattern_examples = "\+.+?###"


compl_mnemo = re.compile(pattern_mnemo, flags=re.DOTALL | re.MULTILINE)
compl_examples = re.compile(pattern_examples, flags=re.DOTALL | re.MULTILINE)

# path_to_mplayer = r"e:\ENG\mplayer\mplayer.exe"
path_to_mplayer = "mplayer"

path_script = os.getcwd()
path_repo = os.path.split(path_script)[0]
path_dir = os.path.join(path_script, "WORDS_NOTEPAD")
path_dir_mp3 = os.path.normpath(os.path.join(path_repo, os.path.join("EnglishSimulate", "Project", "sound_longman_mono")))
path_file_words = os.path.join(path_script, "ПОВТОРИТЬ.txt")
path_last_word = os.path.join(path_script, "last_word.txt")


wait_sound = 180
time_sound_pause = 5
count_sound = 2


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


def sound(word):
    for _ in range(count_sound):
        try:
            path_sound_file = os.path.normpath(os.path.join(path_dir_mp3, f"{word}.mp3"))
            if not os.path.exists(path_sound_file):
                print(f"Не обнаружен файл {path_sound_file}")
            command_list = [path_to_mplayer,  path_sound_file]  #'-delay', '-%s' % time_sound_pause, '-loop', '2',
            command_str = " ".join(command_list)
            # print(f"Выполняется {command_str}")
            process = Popen(command_list, stdout=PIPE, stderr=PIPE)   #, stdout=subprocess.PIPE, stderr=subprocess.PIPE , shell=True, preexec_fn=os.setsid
            stdout, stderr = process.communicate(timeout=5)
        except Exception as e:
            # print(e)
            os.kill(process.pid, signal.SIGTERM)
            return
        time.sleep(time_sound_pause)

def parse_file(word_i):
    path_file = os.path.join(path_dir, f"{word_i}.txt") 
    with open(path_file, encoding="utf-8") as f:

        first_line = f.readline()
        print(first_line) 
        next_data_file = f.read()

        search_mnemo = compl_mnemo.search(next_data_file)
        if search_mnemo:
            mnemo_text = search_mnemo.group("mnemo")
            print(mnemo_text)
            print("#" * 30)

        search_examples = re.findall(pattern_examples, next_data_file)


        #print()


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
        
        sound(word_i)
        write_last_file(path_last_word, word_i)
        time.sleep(wait_sound)
    else:
        start_index = 0
        command = input("Для завершения введите q или enter чтобы продлолжить:\n")
        print("#" * 50)
        if command == "q":
            sys.exit()


