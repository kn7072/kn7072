"""создает файлы для фразовых глоголов."""

import json
import os
import random
from copy import deepcopy

"""
mkdir {a..z} создаст каталоги от a до z

очистить каталоги
find {a..z} -mindepth 1 -exec rm -rf {} +
Как это работает:
find {a..z} — ищет всё внутри папок от a до z.
-mindepth 1 — критически важный параметр: он говорит не применять команду к самим папкам верхнего уровня (глубина 0), а только к их содержимому.
-exec rm -rf {} + — безжалостно удаляет всё найденное.
"""
# отладочные пути
# dir_create_files = "/home/stepan/temp/phrasal_verb"
# path_anki = "/home/stepan/temp/phrasal_verb"

# боевые пути
dir_create_files = "/home/stepan/git_repos/kn7072/ANKI/WORDS"
path_anki = "/home/stepan/git_repos/kn7072/ANKI"
# path_to_phrasal_verb_json = "/home/stepan/git_repos/kn7072/EnglishSimulate/Project/PhrasalVerbs/phrasal_verbs_300.json"
path_to_phrasal_verb_json = "/home/stepan/git_repos/kn7072/EnglishSimulate/Project/PhrasalVerbs/result_added.json"
path_to_ipa = "/home/stepan/git_repos/kn7072/EnglishSimulate/Project/PhrasalVerbs/ipa_for_added_verbs.json"

examples_keys = {
    "comment": [],
    "translate": "",
    "transcription": "",
    "antonyms": [],
    "mnemonic": [],
    "examples": [],
    "example_translate": [],
    "synonyms": [],
    "groups": ["phrasal_verb"],
    "stars": 0,
}


def get_data_file(path_file: str) -> str:
    """Читает файл, и возвращает содержимое."""
    with open(path_file, encoding="utf-8") as f:
        return f.read()


def write_file(path_file: str, data_file: str) -> None:
    """Записывает data_file в файл, перезаписывая сожержимое файла."""
    with open(path_file, encoding="utf-8", mode="w") as f:
        f.write(data_file)


def get_path_file(word: str) -> str:
    """Возвращает путь до файла."""
    first_symbol = word[0].lower()
    path_file_temp = os.path.join(
        dir_create_files, first_symbol, word.lower() + ".json"
    )
    return path_file_temp


ipa_object = json.loads(get_data_file(path_to_ipa))


def prepare_words_content(all_content: dict) -> None:
    for word_i, content_i in all_content.items():
        path_word_i = get_path_file(word_i)
        meanings = content_i["meanings"]
        all_examples = []
        object_for_save = deepcopy(examples_keys)
        translate = ""
        synonyms = ""
        transcription = ipa_object[word_i]
        examples = []
        example_translate = []
        for i, mean_i in enumerate(meanings, 1):
            note_i = f"({note})" if (note := mean_i["synonyms_note"]) else ""
            definition_i = mean_i["definition"]
            tr_i = f"{i}) {definition_i}{note_i} "
            translate += tr_i
            # если заполнен список синонимов - берем его для данного значения
            synonyms_i = mean_i["synonyms"]
            if synonyms_i:
                synonyms += f"{definition_i} - {', '.join(synonyms_i)}\n"
            # забираем примеры и складывам их в общий список - далее его перемешаем
            all_examples.extend(mean_i["examples"])
        random.shuffle(all_examples)
        for example_i in all_examples:
            examples.append(example_i["en"])
            example_translate.append(example_i["ru"])
        object_for_save["translate"] = translate
        object_for_save["synonyms"] = synonyms
        object_for_save["transcription"] = transcription
        object_for_save["examples"] = examples
        object_for_save["example_translate"] = example_translate
        temp_dict = {word_i: object_for_save}
        text_for_save = json.dumps(temp_dict, indent=4, ensure_ascii=False)
        write_file(path_word_i, text_for_save)

        path_notebook = os.path.join(path_anki, "WORDS_NOTEPAD", f"{word_i}.txt")
        # if not os.path.isfile(path_notebook):
        contant_head = f"{word_i} {transcription} {translate}"
        temp_list = [
            f"\n\n{i[0]}\n{i[1]}\n\n####" for i in zip(examples, example_translate)
        ]
        content_all = contant_head + "".join(temp_list)
        with open(path_notebook, encoding="utf-8", mode="w") as f:
            f.write(content_all)


all_content = json.loads(get_data_file(path_to_phrasal_verb_json))
prepare_words_content(all_content)
