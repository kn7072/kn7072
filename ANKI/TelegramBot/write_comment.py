# coding:utf-8
import json
import os
from typing import Union

dir_for_search_files = "/home/stepan/GIT/kn7072/ANKI/WORDS"
list_words = ["worm", "norm"]


def get_data_file(path_file: str) -> str:
    """Читает файл, и возвращает содержимое."""
    with open(path_file, encoding="utf-8") as f:
        return f.read()


def write_file(path_file: str, data_file: str) -> None:
    """Записывает data_file в файл, перезаписывая сожержимое файла."""
    with open(path_file, encoding="utf-8", mode="w") as f:
        f.write(data_file)


def get_path_file(word: str) -> Union[str, None]:
    """Возвращает путь до файла."""
    first_symbol = word[0].lower()
    path_file = None
    path_file_temp = os.path.join(dir_for_search_files, first_symbol, word.lower() + ".json")
    if os.path.isfile(path_file_temp):
        path_file = path_file_temp
    else:
        print(f"Нет файла {path_file_temp}")
    return path_file


for word_i in list_words:
    path_word_i = get_path_file(word_i)
    if path_word_i:
        data_file_i = get_data_file(path_word_i)
        data_file_i_json = json.loads(data_file_i)
        for word, data_word in data_file_i_json.items():
            new_comment_list = data_word["comment"]
            word_lower = word.lower()
            print(word_lower)
            comment_list_lower = [comment_i.lower() for comment_i in data_word["comment"]]
            for word_write_i in list_words:
                if word_write_i != word_lower and word_write_i not in comment_list_lower:
                    new_comment_list.append(word_write_i)
            data_file_i_json[word]["comment"] = new_comment_list
            new_data_json_word_i = json.dumps(data_file_i_json, ensure_ascii=False, indent=4)
            write_file(path_word_i, new_data_json_word_i)
