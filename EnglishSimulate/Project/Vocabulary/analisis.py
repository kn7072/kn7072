# -*- coding: utf-8 -*-
import json
from copy import deepcopy

path_to_json_words = "words.json"
with open(path_to_json_words, encoding="utf-8") as f:
    obj_words = json.loads(f.read())

modificate_obj = deepcopy(obj_words)

name_groups = ["Причастие - сложное подлежащее", "Причастие"]
path_to_words = r"НеличныеФормы\Причастие\СложноеПодлежащее\слова.txt"
list_word = [word_i.strip() for word_i in open(path_to_words, encoding="utf-8")]
# тест
temp = {
        "transcription": "",
        "examples": [],
        "antonyms": [],
        "translate": "",
        "comment": [],
        "mnemonic": [],
        "synonyms": [],
        "grups": ["all_words"]
    }
temp["grups"].extend(name_groups)


def analisis():
    for word_i in list_word:
        find_word = obj_words.get(word_i)
        if find_word:
            modificate_obj[word_i]["grups"].extend(name_groups)
            modificate_obj[word_i]["grups"] = list(set(modificate_obj[word_i]["grups"]))
        else:
            print("Не обнаружено слово %s" % word_i)
            modificate_obj[word_i] = temp


def crate_json_file():
    data_words = json.dumps(modificate_obj, ensure_ascii=False, indent=4)
    with open(r"words.json", mode="w", encoding="utf-8") as f:
        f.write(data_words)
    print()

analisis()
print()
crate_json_file()