# -*- conding: utf-8 -*-
import json
import os

path_to_data_words = r"info_longman.txt"
path_to_data_groups = "group_all.txt"


def get_info_groups():
    info_dict = {}
    current_group = ""
    for line_i in open(path_to_data_groups, "r", encoding="utf-8"):
        if line_i.startswith("####"):
            current_group = line_i.replace("####", "").strip()
            # current_group = nane_i_group
            # info_dict[current_group] = []
        else:
            word_i = line_i.split(" ")[0].strip()
            groups_word_i = info_dict.get(word_i)
            if not groups_word_i:
                info_dict[word_i] = []
                info_dict[word_i].append(current_group)
            else:
                info_dict[word_i].append(current_group)
    return info_dict

info_dict = get_info_groups()

temp_list = []
with open(path_to_data_words, "r", encoding="utf-8") as f:
    temp_list = [i.split(";") for i in f.read().split("\n")]
    temp_list.sort(key=lambda i: i[0])


def get_word(list_word):
    return [word_i.strip().replace(" ", "_") for word_i in list_word]

data_dict = {}
for word_i, translate, transcription in temp_list:
    data_dict[word_i] = {}
    data_dict[word_i]["transcription"] = transcription
    data_dict[word_i]["translate"] = translate
    data_dict[word_i]["grups"] = ["all_words"]
    other_groups = info_dict.get(word_i)
    if other_groups:
        data_dict[word_i]["grups"].extend(other_groups)
    data_dict[word_i]["examples"] = []
    data_dict[word_i]["mnemonic"] = []
    data_dict[word_i]["synonyms"] = []
    data_dict[word_i]["antonyms"] = []
    data_dict[word_i]["comment"] = []

data_words = json.dumps(data_dict, ensure_ascii=False, indent=4)

with open(r"words_DEBUG.json", mode="w", encoding="utf-8") as f:
    f.write(data_words)
print()
