# -*- coding:utf-8 -*-

import time
import os
import re
import json
import requests

url = "https://wooordhunt.ru"

all_examples = "<div class=\"block\">(?P<text>.+?)</div>"
compl_all_examples = re.compile(all_examples)

eng_example = "<p class=\"ex_o\">(?P<text>.+?)<"
comp_eng_example = re.compile(eng_example)

rus_example = "<p class=\"ex_t human\">(?P<text>.+?)<"
comp_rus_example = re.compile(rus_example)


################################################
temp_1 = "id=\"audio_us\"(?P<text>.+)id=\"audio_uk\""
temp_1 = "id=\"us_tr_sound\"(?P<text>.+)id=\"uk_tr_sound\""
compl_1 = re.compile(temp_1)

temp_sound = "src=\"(?P<path_sound>.*?.mp3)\""
compl_sound = re.compile(temp_sound)

temp_trans = "transcription\">(?P<transcription>.*?)<"
compl_trans = re.compile(temp_trans)

temp_translate = "t_inline_en\">(?P<translate>.+?)<"
compl_translate = re.compile(temp_translate)


path_union = "union.txt"
path_json_origin = "words_new.json"


path_html_words = "HTML_WORDS"
paht_json_obj = "JSON_EXAMPLES"


def get_origin_json(path_to_json):
    with open(path_to_json, encoding="utf-8") as f:
        data = f.read()
        return json.loads(data)


def get_list_words(path_to_file):
    temp = list()
    for i in open(path_to_file, encoding="utf-8"):
        temp.append(i.rstrip())
    return temp


def get_list_words_union(path_union):
    list_words = []
    with open(path_union, encoding="utf-8") as f:
        for word_i in f:
            list_words.append(word_i.replace("\n", ""))
    return list_words


def diff_words(list_union, list_origin):
    return set(list_union) - set(list_origin)


def create_file(data_json, name_file):
    str_json = json.dumps(data_json, ensure_ascii=False, indent=4)
    with open(name_file, mode="w", encoding="utf-8") as f:
        f.write(str_json)


def create_html(path_to_file, data_file):
    with open(path_to_file, mode="wb") as f:
        f.write(data_file)


def get_example(path_to_html):

    name = os.path.split(path_to_html)[1].split(".")[0] + ".json"
    path_json = os.path.join(paht_json_obj, name)
    # if os.path.isfile(path_json):
    #     return

    with open(path_to_html, encoding="utf-8") as f:
        data_html = f.read()

    search = compl_all_examples.search(data_html)
    dict_examples = {"examples_eng" : [],
                     "examples_rus": []}
    try:
        all_text = search.group("text")
        all_text = all_text.replace("</b>", "").replace("<b>", "")
        search_eng = re.findall(comp_eng_example, all_text)
        search_rus = re.findall(comp_rus_example, all_text)
        if len(search_eng) == len(search_rus):

            search_eng = [i.replace("&nbsp;", "").replace(";", ".,").strip() for i in search_eng]
            search_rus = [i.replace("&nbsp;", "").replace(";", ".,").strip() for i in search_rus]
            dict_examples = {"examples_eng" : search_eng,
                             "examples_rus": search_rus}
            str_json = json.dumps(dict_examples, ensure_ascii=False, indent=4)
            with open(path_json, mode="w", encoding="utf-8") as f:
                f.write(str_json)
        else:
            print("Количество примеров и переводов отличаются %s" % path_to_html)
    except AttributeError as e:
        print("Проблемы с %s\ %s" % (path_to_html, e))
    return dict_examples


def create_sound_file(name, data_file, path_dir):
    path_to_file = os.path.join(path_dir, "%s.mp3" % name)
    with open(path_to_file, mode="wb") as f:
        f.write(data_file)


def get_info_word(word, path_create_sound="audio"):
    url_word = "%s/word/%s" % (url, word)
    r = requests.get(url_word)
    data_html_bin = r.content # r.text
    data_html = r.text

    path_to_file = os.path.join(path_html_words, "%s.html" % word)
    create_html(path_to_file, data_html_bin)
    dict_examples = get_example(path_to_file)

    search = compl_1.search(data_html)
    all_test = search.group("text")

    search_sound = compl_sound.search(all_test)
    if search_sound:
        paht_to_sound = search_sound.group("path_sound")
        all_path = url + paht_to_sound
        data_sound = requests.get(all_path)
        path_dir_sounds = os.path.join(os.getcwd(), path_create_sound)
        create_sound_file(word, data_sound.content, path_dir_sounds)
    else:
        print(f"Не найдет mp3 файл для {word}")    

    search_transcription = compl_trans.search(all_test)
    transcription = search_transcription.group("transcription")

    search_translate = compl_translate.search(data_html)
    translate = search_translate.group("translate")
    return translate, transcription, dict_examples


# for file_i in os.listdir(path_html_words):
#     path_file = os.path.join(path_html_words, file_i)
#     get_example(path_file)


########################################################################################################
#