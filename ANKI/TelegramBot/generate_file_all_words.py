# coding: utf-8
import json
import os

from common import get_data_file, get_mnemo_list, path_anki, read_file

data_all_words = read_file("ALL_WORDS.txt")
dir_for_search_files = r"/home/stepan/GIT/kn7072/ANKI/WORDS"


def get_path_file(word: str) -> str:
    """Возвращает путь до файла."""
    first_symbol = word[0].lower()
    path_file = None
    path_file_temp = os.path.join(dir_for_search_files, first_symbol, word.lower() + ".json")
    if os.path.isfile(path_file_temp):
        path_file = path_file_temp
    else:
        print(f"Нет файла {path_file_temp}")
    return path_file


def write_file(path_file: str, data_file: str) -> None:
    """Записывает data_file в файл, перезаписывая сожержимое файла."""
    with open(path_file, encoding="utf-8", mode="w") as f:
        return f.write(data_file)


list_exists_mnemo = []
error_list = []
god_object = {}

for word_i in data_all_words:
    path_word_i = get_path_file(word_i)
    if path_word_i:
        data_file_i = get_data_file(path_word_i)
        data_file_i_json = json.loads(data_file_i)

        word_key = list(data_file_i_json.keys())[0]
        mnemonic_word = data_file_i_json[word_key]["mnemonic"]
        data_word_i = god_object.get(word_i)
        if data_word_i:
            print("Слово уже встечалось")
        else:
            god_object[word_i] = data_file_i_json[word_key]
    else:
        print(f"ПРОБЛЕМЫ С {word_i}")
        error_list.append(word_i)
else:
    file_name_all_words = "all_words.json"
    write_file(file_name_all_words, json.dumps(god_object, ensure_ascii=False, indent=4))
