# -*- coding:utf-8 -*-
import os
from common import get_list_words, get_info_word, get_origin_json, create_file
from copy import deepcopy
import json

path_script = os.getcwd()
path_anki = os.path.split(path_script)[0]
path_words = os.path.join(path_anki, "words.json")

examples_keys = {
        "comment": [],
        "translate": "",
        "transcription": "",
        "antonyms": [],
        "mnemonic": [],
        "examples": [],
        "example_translate": [],
        "synonyms": [],
        "grups": [
            "all_words"
        ]
    }


all_words = get_origin_json(path_words)
print(len(all_words))

path_file_to_save = os.path.join(os.getcwd(), "new_words.txt")

temp_list_words = []


def create_json_word(word_i):
    translate, transcription, dict_examples = get_info_word(word_i)
    copy_temp = deepcopy(examples_keys)
    copy_temp["transcription"] = transcription
    copy_temp["translate"] = translate
    copy_temp["examples"] = dict_examples["examples_eng"]
    copy_temp["example_translate"] = dict_examples["examples_rus"]
    temp_dict = {word_i: copy_temp}
    dir_for_create_json = os.path.join(path_anki, "WORDS", word_i[0].lower(), f"{word_i}.json")
    path_notebook = os.path.join(path_anki, "WORDS_NOTEPAD", f"{word_i}.json")
    if not os.path.isfile(path_notebook):
        contant_head = f"{word_i} {transcription} {translate}"
        temp_list = [f"\n\n{i[0]}\n{i[1]}\n\n####" for i in zip(dict_examples["examples_eng"], dict_examples["examples_rus"])]
        content_all = contant_head + "".join(temp_list)
        with open(path_notebook, encoding="utf-8", mode="w") as f:
            f.write(content_all)

    with open(dir_for_create_json, encoding="utf-8", mode="w") as f:
        f.write(json.dumps(temp_dict, ensure_ascii=False, indent=4))
    temp_list_words.append([word_i, translate, transcription])


def update_word_dict():
    """Обновляет обищий файл words.json"""
    temp_dict = {}
    for word_i, translate, transcription in temp_list_words:
        copy_temp = deepcopy(examples_keys)
        copy_temp["transcription"] = transcription
        copy_temp["translate"] = translate
        temp_dict[word_i] = copy_temp
    all_words.update(temp_dict)
    create_file(all_words, path_words)


list_new_words = get_list_words(path_file_to_save)
for word_i in list_new_words:
    if word_i in all_words:
        # print("Слово уже содержится в списке")
        pass
    else:
        print(f"{word_i}")
        try:
            create_json_word(word_i)
        except Exception as e:
            print(f"Проблемы {word_i}\n{e}")

update_word_dict()
print(list_new_words)

