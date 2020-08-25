# -*- coding:utf-8 -*-
import json
import os
import re

path_to_json_file = "words.json"
name_file = "words_txt.txt"

def get_data():
    list_data = []
    with open(path_to_json_file, encoding="utf-8") as f:
        data = f.read()
        dict_data = json.loads(data)
    for key, val in dict_data.items():
        list_data.append([key, val["transcription"], val["translate"]])
    list_data.sort(key=lambda i: i[0])
    return list_data


def create_file(list_data):
    with open(name_file, mode="w", encoding="utf-8") as f:
        for word_i in list_data:
            info = ";".join(word_i) + "\n"
            f.write(info)

data = get_data()
if not os.path.isfile(name_file):
    create_file(data)

def get_search_words(pattern, list_data):
    list_words = []
    for word_i, _, _ in list_data:
        match = re.search(pattern, word_i)
        if match:
            list_words.append(word_i)
    return list_words

def print_search(list_words):
    for ind, i in enumerate(list_words):
        print(ind, "   ", "англ:%s" % i, "   ", i)

reg_pat = ".*?ment"
list_words = get_search_words(reg_pat, data)
print_search(list_words)
# print(list_words)

