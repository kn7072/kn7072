# -*- coding: utf-8 -*-
import json
import os

path_to_json_file = "words.json"
path_file_1 = "4000 Essential English Words_1.txt"
path_file_2 = "4000 Essential English Words_2.txt"



def parser_file_1(path_file):
    data_word = {}
    with open(path_file, "r", encoding="utf-8") as f:
        for i in f:
            temp_ = i.split("\t")
            data_word[temp_[2]] = {"img": temp_[1], "transcription": temp_[3], "sound": temp_[4]}
    return data_word

def parser_file_2(path_file):
    data_word = {}
    with open(path_file, "r", encoding="utf-8") as f:
        for i in f:
            temp_ = i.split("\t")
            data_word[temp_[0]] = {"img": temp_[1],
                                   "transcription": temp_[7],
                                   "sound": temp_[2],
                                   "sound_meaning": temp_[3],
                                   "sound_example": temp_[4],
                                   "meaning": temp_[5],
                                   "example": temp_[6]
                                   }
    return data_word

data_file_1 = parser_file_1(path_file_1)
data_file_2 = parser_file_2(path_file_2)
data_file_1.update(data_file_2)

def analisis_words(data_json, data_4000, paht_macm="Macmillan.txt"):
    """Разделяет слова на группы"""
    not_found_words = []
    with open(paht_macm, "r", encoding="utf-8") as f:
        list_mack = [word.strip() for word in f]
    keys_our = list(data_json.keys())
    keys_4000 = list(data_4000.keys())
    diff_1 = set(keys_our) - set(keys_4000)
    diff_2 = set(keys_4000) - set(keys_our)

    diff_3 = set(keys_our) - set(list_mack)
    diff_4 = set(keys_4000) - set(list_mack)
    print(len(diff_1))
    print(len(diff_2))
    print(len(diff_3))
    print(len(diff_4))
    pass


# def analisis_words(data_json, data_4000):
#     """Разделяет слова на группы"""
#     not_found_words = []
#     for word_i, value_i in data_json.items():
#         pass
with open(path_to_json_file, "r", encoding="utf-8") as f:
    data_json = json.loads(f.read())

analisis_words(data_json, data_file_1)
# res = analisis_json(data_json)