# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE
import os
import json
import sys
import itertools
import datetime

# d:\фильмы\АНГЛИЙСКИЙ\Самвел Гарибян - Чудо-словарь Самвела Гарибяна. Английский без английского - 2008

# sys.putenv('PYTHONIOENCODING', 'utf8')


path_dir_files = "d:\kn7072\ANKI\WORDS"
path_dir_for_notepad = "d:\kn7072\ANKI\WORDS_NOTEPAD"


def create_file_for_notepad(word_i, path_file):
    with open(path_file, encoding="utf-8", mode="r") as f:
        try:
            data_json = json.loads(f.read())
            word_i = word_i.split(".json")[0]
            data_json_word = data_json[list(data_json.keys())[0]]
            list_exercises = list(zip(data_json_word["examples"], data_json_word["example_translate"]))
            data_to_notepad = ["\n%s\n%s\n\n####\n" % (eng, rus) for eng, rus in list_exercises]
            data_to_notepad = word_i + " "+ data_json_word["transcription"] + " "+ data_json_word["translate"] + "\n" + "".join(data_to_notepad)
            # examples example_translate
        except:
            print()

    path_notepad = os.path.join(path_dir_for_notepad, "%s.txt" % word_i)
    with open(path_notepad, encoding="utf-8", mode="w") as f:
        f.write(data_to_notepad)


def create_files_exersises():
    list_dir_word = os.listdir(path_dir_files)
    for dir_word_i in list_dir_word:
        path_dir_word_i = os.path.join(path_dir_files, dir_word_i)
        for word_i in os.listdir(path_dir_word_i):
            path_world_i = os.path.join(path_dir_word_i, word_i)
            create_file_for_notepad(word_i, path_world_i)

    pass

def show_exercises(path_file_open):
    # "-qt 1111" -заполняет файл
    # , "-filePath D:\\kn7072\\ANKI\\FIRST.txt"
    # args = [r"C:\Program Files (x86)\Notepad++\notepad++.exe", "D:\\kn7072\\ANKI\\FIRST.txt","-multiInst", "-nosession",  "-qt 1111\n"]
    args = [r"C:\Program Files (x86)\Notepad++\notepad++.exe", path_file_open, "-multiInst", "-nosession"]
    proc = Popen(args, stdout=PIPE, stderr=PIPE)
    return proc

def get_list_passed_words():
    with open("passed_words.txt", encoding="utf-8") as f:
        data = f.read()
        list_words = [i for i in data.split(";") if i]
    return list_words

def updata_words(list_new_words, fine_name="passed_words.txt"):
    all_list = ";".join(list_new_words) + ";"
    with open(fine_name, encoding="utf-8", mode="a") as f:
        f.write(all_list)

def get_first_line(path_file):
    with open(path_file, encoding="utf-8") as f:
        return f.readline()

def generate_file_passed(count_words):
    all_words = set(os.listdir(path_dir_for_notepad))  # все слова
    passed_words = set(get_list_passed_words())  # пройденные слова
    unpassed_words = all_words - passed_words  # слова которые только предстоит изучить
    slice_words = set(itertools.islice(unpassed_words, 0, count_words))  # выбираем count_words слов из списка НЕИЗУЧЕННЫХ
    unpassed_words.difference_update(slice_words)  # список слов - из всех слов которые нужно изучить - вычитаем слова из списка slice_words
    # складываем new_words и пройденные (passed_words) = запишим эти слова в файл - как пройденные и скрипт будет выдавать слова только из списка slice_words
    passed_words.update(unpassed_words)
    updata_words(list(passed_words), fine_name="passed_words_new.txt")


file_memonic_learnd = "mnemonic_words.txt"
def save_file(shown_words):
    temp = "%s;%s\n"
    delimetr = "#" * 30 + "\n"
    dt = datetime.date.today()
    if not os.path.isfile(file_memonic_learnd):
        with open(file_memonic_learnd, encoding="utf-8", mode="w") as f:
            for word_i in shown_words:
                f.write(temp % (word_i, dt))
            f.write(delimetr)
    else:
        with open(file_memonic_learnd, encoding="utf-8", mode="a") as f:
            for word_i in shown_words:
                f.write(temp % (word_i, dt))
            f.write(delimetr)

# generate_file_passed(1500)

# show_exercises()
# create_files_exersises()

# {{(?P<mnemo>.+?)}}
# \+.+?####
unpassed_words = set(os.listdir(path_dir_for_notepad)) - set(get_list_passed_words())
list_shown_words = []
for ind, name_file in enumerate(unpassed_words):
    path_file_open = os.path.join(path_dir_for_notepad, name_file)
    info_word = get_first_line(path_file_open)# .encode("utf-8").decode("cp866")
    print(str(ind) + "   " + info_word)
    # sys.stdout.write(info_word)

    proc = show_exercises(path_file_open)
    list_shown_words.append(name_file)
    res = input()
    proc.kill()
    if res == "q":
        updata_words(list_shown_words)
        save_file(list_shown_words)
        sys.exit(0)
print()