# coding: utf-8

"""Описание модуля."""
import json
import os

from common import read_file

path_to_sentence = "../Предложения.txt"
path_to_all_words = "all_words.json"
path_to_sentence_new = "../Предложения_new.txt"
dir_for_search_files = r"../WORDS"


def get_data_file(path_file: str) -> None:
    """Возвращает содержимое файла."""
    with open(path_file, encoding="utf-8") as f:
        return f.read()


def write_file(path_file: str, data_file: str) -> None:
    """Записывает data_file в файл, перезаписывая сожержимое файла."""
    with open(path_file, encoding="utf-8", mode="w") as f:
        return f.write(data_file)


def get_list_sentence(path_file: str) -> list:
    """Возврщает список предложений."""
    list_sentence = []
    for i in open(path_file, mode="r", encoding="utf-8"):
        list_sentence.append(i.split(";")[1].strip())
    return list_sentence


def get_all_sentence() -> set:
    """Возвращает все примеры."""
    all_sentence = set()

    for _, data_word_i in data_all_words.items():
        for example_i in data_word_i["examples"]:
            all_sentence.add(example_i)
    return all_sentence


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


def search_word_for_sentence(list_sentence: set) -> dict:
    """Возвращает словарь, ключами которого являются предложения, а значние - список слов входящий в это предложение."""
    find_sentence = {}
    for word_i, data_word_i in data_all_words.items():
        for num_example, example_i in enumerate(data_word_i["examples"]):
            if example_i in list_sentence:
                if find_sentence.get(example_i):
                    find_sentence[example_i]["words"].append(word_i)
                else:
                    find_sentence[example_i] = {}
                    find_sentence[example_i]["words"] = []
                    find_sentence[example_i]["translate"] = data_word_i["example_translate"][num_example]
                    find_sentence[example_i]["words"].append(word_i)
    return find_sentence


def get_data_all_word(all_examples: dict) -> dict:
    """Возвращает данные по всем словам."""
    god_object = {}

    def modified_examples(examples_list: list) -> list:
        """Возвращает модифицированный список примеров."""
        temp_list = []
        for example_i in examples_list:
            temp_list.append((example_i, all_examples[example_i]))
        return temp_list

    for word_i in data_all_words:
        path_word_i = get_path_file(word_i)
        if path_word_i:
            data_file_i = get_data_file(path_word_i)
            data_file_i_json = json.loads(data_file_i)
            word_key = list(data_file_i_json.keys())[0]
            is_known = god_object.get(word_i)
            if is_known:
                print("Слово уже встечалось")
            else:
                data_word_i = data_file_i_json[word_key]
                examples = modified_examples(data_word_i["examples"])
                data_word_i["examples"] = examples
                god_object[word_i] = data_word_i
        else:
            print(f"ПРОБЛЕМЫ С {word_i}")
            raise Exception("Нет файла")
    else:
        file_name_all_words = "all_words_new.json"
        write_file(file_name_all_words, json.dumps(god_object, ensure_ascii=False, indent=4))


data_all_words = json.loads(get_data_file(path_to_all_words))
list_sentence = get_list_sentence(path_to_sentence)
find_sentence = search_word_for_sentence(list_sentence)

# list_sentence_all_words = get_all_sentence()
# find_all_sentence = search_word_for_sentence(list_sentence_all_words)
# get_data_all_word(find_all_sentence)


for number, sentence_i in enumerate(list_sentence, start=1):
    if sentence_i not in find_sentence:
        print(number, sentence_i)

text_sentence = ""
for sentence_i, value_sentence_i in find_sentence.items():
    words = value_sentence_i["words"]
    text_sentence += f"{', '.join(words)};    {sentence_i};    {value_sentence_i['translate']}\n"
    # if len(words) > 1:
    #     text_sentence += f"{', '.join(words)};    {sentence_i}"
    # else:
    #     text_sentence += f"{words[0]};    {sentence_i}\n"

write_file(path_to_sentence_new, text_sentence)
print()



