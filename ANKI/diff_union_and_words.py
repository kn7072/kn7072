# -*- coding: utf-8 -*-
import json
from parsing.parser_db import get_info_word, html_word
import time
import os
import re

all_examples = "<div class=\"block\">(?P<text>.+?)</div>"
compl_1 = re.compile(all_examples)

eng_example = "<p class=\"ex_o\">(?P<text>.+?)<"
comp_eng_example = re.compile(eng_example)

rus_example = "<p class=\"ex_t human\">(?P<text>.+?)<"
comp_rus_example = re.compile(rus_example)

path_union = "union.txt"
path_json_origin = "words_new.json"


def get_origin_json(path_to_json):
    with open(path_to_json, encoding="utf-8") as f:
        data = f.read()
        return json.loads(data)

def get_list_words_union(path_union):
    list_words = []
    with open(path_union, encoding="utf-8") as f:
        for word_i in f:
            list_words.append(word_i.replace("\n", ""))
    return list_words

def diff_words(list_union, list_origin):
    return set(list_union) - set(list_origin)

def create_file(data_json, name_file):
    str_json = json.dumps(data_json, ensure_ascii=False, indent=4)
    with open(name_file, mode="w", encoding="utf-8") as f:
        f.write(str_json)

# list_words_union = get_list_words_union(path_union)
# origin_json = get_origin_json(path_json_origin).keys()

    # diff = diff_words(list_words_union, origin_json)
    # print(len(diff))
    # with open("diff.txt", mode="w", encoding="utf-8") as f:
    #     for i in diff:
    #         f.write(i + "\n")

# list_diff = get_list_words_union("diff_finale.txt")
# path_create_sound = r"d:\kn7072\EnglishSimulate\Project\sound_longman_mono"
# temp_list = []
# for word_i in list_diff:
#     info_word = get_info_word(word_i, path_create_sound=path_create_sound)
#     temp_list.append(info_word)
########################################################################################################
# $(".block")
path_html_words = "HTML_WORDS"
paht_json_obj = "JSON_EXAMPLES"
def get_example(path_to_html):

    name = path_to_html.rsplit("\\", 1)[1].split(".")[0] + ".json"
    path_json = os.path.join(paht_json_obj, name)
    if os.path.isfile(path_json):
        return

    with open(path_to_html, encoding="utf-8") as f:
        data_html = f.read()
    search = compl_1.search(data_html)
    try:
        all_text = search.group("text")
        # if "according to" in path_json:
        #     print()
        all_text = all_text.replace("</b>", "").replace("<b>", "")
        # search_eng = comp_eng_example.search(all_text)
        # search_rus = comp_rus_example.search(all_text)
        search_eng = re.findall(comp_eng_example, all_text)
        search_rus = re.findall(comp_rus_example, all_text)
        if len(search_eng) == len(search_rus):

            search_eng = [i.replace("&nbsp;", "").replace(";", ".,").strip() for i in search_eng]
            search_rus = [i.replace("&nbsp;", "").replace(";", ".,").strip() for i in search_rus]
            dict_examples = {"examples_eng" : search_eng,
                             "examples_rus": search_rus}
            str_json = json.dumps(dict_examples, ensure_ascii=False, indent=4)
            with open(path_json, mode="w", encoding="utf-8") as f:
                f.write(str_json)
        else:
            print("Количество примеров и переводов отличаются %s" % path_to_html)
    except AttributeError as e:
        print("Проблемы с %s\ %s" % (path_to_html, e))


for file_i in os.listdir(path_html_words):
    path_file = os.path.join(path_html_words, file_i)
    get_example(path_file)


########################################################################################################
# origin_json = get_origin_json(path_json_origin)
#
# for ind, word_i in enumerate(origin_json.keys()):
#     time.sleep(0.2)
#     if ind >= 100 and ind % 100 == 0:
#         print("100")
#     html_word(word_i, path_html_words)
########################################################################################################
# temp_list = [('finely', 'тонко, хорошо, прекрасно, превосходно, ясно, точно, мелко', ' |ˈfaɪnli|')]
# for word_i, transl, transcription in temp_list:
#     obj = {
#         "comment": [],
#         "translate": transl,
#         "transcription": transcription,
#         "antonyms": [],
#         "mnemonic": [],
#         "examples": [],
#         "example_translate": [],
#         "synonyms": [],
#         "grups": [
#             "all_words"
#         ]
#     }
#
#     origin_json[word_i] = obj
#     print()
# # into_db(path_db, "longman_base", temp_list)
# origin_json = {k: v for k, v in sorted(origin_json.items(), key=lambda item: item)}
# create_file(origin_json, "words.json")
########################################################################################################

print()

