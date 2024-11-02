# coding: utf-8

"""Модуль создает каталог с двумя файлами: предложений на английском и файл с переводом."""

import json
import os

from common import get_data_file

path_to_known_examples = "../Предложения.txt"
file_to_save_words = "WORDS_FOR_LEARN.txt"
dir_name_for_save_sentence = "./SENTENCE"
path_to_eng_sentence = os.path.join(dir_name_for_save_sentence, "ENG.txt")
path_to_rus_sentence = os.path.join(dir_name_for_save_sentence, "RUS.txt")
path_to_all_words = "all_words_new.json"
all_words_json = json.loads(get_data_file(path_to_all_words))


def get_study_words() -> set:
    """Возвращает уникальные слова."""
    temp_words = set()
    for line_i in open(file_to_save_words, encoding="utf-8"):
        if line_i and line_i != "##########":
            temp_words.add(line_i.strip())
    return temp_words


def get_know_words() -> dict:
    """Возвращаем множество изученных слов."""
    all_word_dict = {}
    for str_i in open(path_to_known_examples, encoding="utf-8"):
        str_i = str_i.strip()
        if str_i:
            know_words_str, example_eng, example_rus = str_i.split(";")
            know_words_list = [word_i.strip() for word_i in know_words_str.split(",")]
            for known_word_i in know_words_list:
                is_added = all_word_dict.get(known_word_i)
                if is_added:
                    all_word_dict[known_word_i]["examples"].append(
                        (example_eng, example_rus, know_words_str)
                    )
                else:
                    all_word_dict[known_word_i] = {}
                    all_word_dict[known_word_i]["examples"] = []
                    all_word_dict[known_word_i]["examples"].append(
                        (example_eng, example_rus, know_words_str)
                    )
    return all_word_dict


def create_file_sentence(know_all_words: dict, study_words: set) -> None:
    """Создаем файлы с предложениями для изучаемых слов."""
    temp_dict = {}
    for word_i in study_words:
        try:
            for example_eng, example_rus, know_words_str in know_all_words[word_i]["examples"]:
                temp_dict[example_eng] = [example_rus, know_words_str]
        except KeyError:
            print(f"Проблемное слово {word_i}")

    f_eng = open(path_to_eng_sentence, encoding="utf-8", mode="w")
    f_rus = open(path_to_rus_sentence, encoding="utf-8", mode="w")
    try:
        for sentence_eng, valume in temp_dict.items():
            f_eng.write(f"{sentence_eng}\n")
            f_rus.write(f"{valume[0]};    {valume[1]}\n")
    finally:
        f_eng.close()
        f_rus.close()


know_all_words = get_know_words()  # слова у которых выбраны предложения
study_words = get_study_words()  # изучаемые слова
create_file_sentence(know_all_words, study_words)
print()
