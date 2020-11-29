# -*- coding: utf-8 -*-
import os
import re


token = "1425771819:AAEcMh29JkNKEejduDdf2T52m0eJrecWq6o"
chat_id_list = ["344022850", "366602173"]


pattern_mnemo = "{{(?P<mnemo>.+?)}}"
pattern_examples = "\+.+?###"


compl_mnemo = re.compile(pattern_mnemo, flags=re.DOTALL | re.MULTILINE)
compl_examples = re.compile(pattern_examples, flags=re.DOTALL | re.MULTILINE)

# path_to_mplayer = r"e:\ENG\mplayer\mplayer.exe"
path_to_mplayer = "mplayer"

path_script = os.getcwd()
path_anki = os.path.split(path_script)[0]
path_repo = os.path.split(path_anki)[0]
path_dir = os.path.join(path_anki, "WORDS_NOTEPAD")
path_dir_mp3 = os.path.normpath(os.path.join(path_repo, os.path.join("EnglishSimulate", "Project", "sound_longman_mono")))
path_file_words = os.path.join(path_script, "ПОВТОРИТЬ.txt")
path_last_word = os.path.join(path_script, "last_word.txt")

wait_sound = 360
time_sound_pause = 5
count_sound = 2




# get_me = f"https://api.telegram.org/bot{token}/getMe"
# getupdates = f"https://api.telegram.org/bot{token}/getUpdates"
# print(get_me)
# print(getupdates)

# res = requests.get(getupdates)
# chat_id = res.json()["result"][0]["message"]["chat"]["id"]