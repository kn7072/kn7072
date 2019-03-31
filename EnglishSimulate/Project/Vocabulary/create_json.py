# -*- conding: utf-8 -*-
import json
import os

{
"name_1": {
  "grups": [],
  "links_word": [],
  "transcription": "",
  "translate": "",
  "example": [],
  "mnemonic": [],

}
}

path_to_data_words = r"info_longman.txt"

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
    data_dict[word_i]["examples"] = []
    data_dict[word_i]["mnemonic"] = []
    data_dict[word_i]["synonyms"] = []
    data_dict[word_i]["antonyms"] = []

data_words = json.dumps(data_dict, ensure_ascii=False, indent=4)

with open(r"words.json", mode="w", encoding="utf-8") as f:
    f.write(data_words)
print()
