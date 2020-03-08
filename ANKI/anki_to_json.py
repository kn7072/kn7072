# -*- coding: utf-8 -*-
import json

path_export_file = r"d:\ЭКСПЕРИМЕНТЫ АНКИ\My_English_words_ЗАПИСИ_В_ТЕКСТ.txt"
path_json_origin = r"words.json"

structure_data = {
    "translate": "",
    "word_i" : "",
    "transcription" : "",
    "sound_word" : "",
    "mnemonic" : "",
    "example" : ""
}

temp_list_example = []

def create_data(line):
    structure_data = {
        "translate": "",
        "word_i": "",
        "transcription": "",
        "sound_word": "",
        "mnemonic": [],
        "examples": []
    }
    data = line.replace("\n", "").split("\t")

    structure_data["translate"] = data[0]
    structure_data["word_i"] = data[1]
    structure_data["transcription"] = data[2]
    structure_data["sound_word"] = data[3]
    structure_data["mnemonic"] = data[4]
    if data[5]:
        temp_list_example.append([data[1], data[5]])

        # todo 3 строчки нижу нужно переписать после формирования окончательного шаблона(выгружаемого с anki)
        list_example = [i.strip() + "." for i in data[5].split(".") if i]  # [i.strip() + ". #" for i in data[5].split(".") if i]
        # убираем последнюю решетку в последнем примере
        list_example[-1] = list_example[-1].rsplit("#", 1)[0].strip()

        structure_data["examples"] = list_example
    return structure_data


def get_json_from_export_anki(path_export_file):
    """

    :param path_export_file:
    :return:
    """
    json_data = {}
    with open(path_export_file, encoding="utf-8") as f:
        for line_i in f:
            data_word_i = create_data(line_i)
            word_i = data_word_i.pop("word_i")
            json_data[word_i] = data_word_i
    return json_data

def get_origin_json(path_to_json):
    with open(path_to_json, encoding="utf-8") as f:
        data = f.read()
        return json.loads(data)

def update_json(anki_json, origin_json):
    try:
        for word_i, val_i in anki_json.items():
            val_origin = origin_json[word_i]
            if val_i["examples"]:
                val_origin["examples"] = val_i["examples"]
            val_origin["example_translate"] = []
    except KeyError as e:
        print(word_i)

def create_file(data_json, name_file):
    str_json = json.dumps(data_json, ensure_ascii=False, indent=4)
    with open(name_file, mode="w", encoding="utf-8") as f:
        f.write(str_json)


json_data_anki = get_json_from_export_anki(path_export_file)
origin_json = get_origin_json(path_json_origin)
update_json(json_data_anki, origin_json)
create_file(origin_json, "words_new.json")
print()