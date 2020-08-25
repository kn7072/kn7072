# -*- coding: utf-8 -*-
import json
import os

path_words_structure = "WORDS"
path_examples_dir = "JSON_EXAMPLES"
path_origin_file = "words.json"

def get_origin_json(path_to_json):
    with open(path_to_json, encoding="utf-8") as f:
        data = f.read()
        return json.loads(data)


def create_file_json(data_json, name_file):
    str_json = json.dumps(data_json, ensure_ascii=False, indent=4)
    with open(name_file, mode="w", encoding="utf-8") as f:
        f.write(str_json)

def craate_file(path_file, data):
    with open(path_file, mode="w", encoding="utf-8") as f:
        f.write(data)

def create_structure(obj):
    for word_i, val_i in obj.items():
        dir_word = os.path.join(path_words_structure, word_i[0].lower())
        if not os.path.isdir(dir_word):
            os.mkdir(dir_word)
        path_file = os.path.join(dir_word, word_i.lower() + ".json")
        temp_obj = json.dumps({word_i: val_i}, ensure_ascii=False, indent=4)
        craate_file(path_file, temp_obj)

def get_data_file(path_file):
    with open(path_file, encoding="utf-8") as f:
        data = f.read()
    return json.loads(data)

def extend_obj(obj):
    temp_obj = {}
    for word_i, val_i in obj.items():
        temp_obj[word_i] = val_i
        path_to_examples = os.path.join(path_examples_dir, word_i + ".json")
        if not os.path.isfile(path_to_examples):
            print("Не обнаружен файл с примерами %s" % word_i)
            continue
        examples_dict = get_data_file(path_to_examples)
        val_i["examples"] = examples_dict["examples_eng"]
        val_i["example_translate"] = examples_dict["examples_rus"]
    return temp_obj


origin_json = get_origin_json(path_origin_file)
full_origin_json = extend_obj(origin_json)
create_file_json(full_origin_json, "full_words.json")
create_structure(full_origin_json)


