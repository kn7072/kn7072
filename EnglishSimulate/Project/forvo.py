#coding="utf-8"
import requests
import re
import os
import time

parent_re_word = r'id=\"language-container-ru\"(.)+?<article class=\"pronunciations\">(?P<content>.+?)article>'
compl_parent_re_word = re.compile(parent_re_word, re.DOTALL)

parent_re_phrase = r'<article class=\"pronunciations\">(?P<content>.+?)article>'
compl_parent_re_phrase = re.compile(parent_re_phrase, re.DOTALL)

id_re = r'id=\"play_(?P<id>.+?)\"'
compl_id_re = re.compile(id_re, re.DOTALL)

from lxml import etree
from io import StringIO, BytesIO

list_word = []
with open("info_longman.txt", "r", encoding="utf-8") as f:
    list_word = f.read().split("\n")


def get_word(list_word):
    word_i = None
    # for i in list_word:
    #     word_i = i.strip()
        # if len(word_i.split(" "))>1:
        #     continue
        # else:
        #     word_i = word_i
        #     break
    #return word_i
    return list_word[0]

# word, transl, transk = list_word[0].split(";")
# transl_list = transl.split(",")
# word_search = get_word(transl_list)


host = "https://ru.forvo.com"

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 OPR/57.0.3098.116',
                        "Refere": "https://ru.forvo.com/login/"})

login_url = "https://ru.forvo.com/login/"
request = {"login": "forvo100119", "password": "280286w"}
response = session.request(method="POST", data=request, url=login_url)
error_list = {}
print()

dir_rus_word = "longman_rus"
# https://ru.forvo.com/phrase/хранить_в_тайне/#ru

def create_sound_file(word_or_phrase, name_file):
    is_created = False
    temp_url = "https://ru.forvo.com/{word_or_phrase}/{content}/#ru"
    url_word = temp_url.format(word_or_phrase=word_or_phrase, content=name_file)  # "phrase"

    path_create_rus_file = os.path.join(dir_rus_word, "%s_rus.mp3" % name_file)
    if os.path.isfile(path_create_rus_file):
        is_created = True
        return is_created
    response_data = session.request(method="GET", url=url_word)
    contant = response_data.content

    if word_or_phrase == "word":
        search_word = compl_parent_re_word.search(contant.decode())
    else:
        search_word = compl_parent_re_phrase.search(contant.decode())

    if search_word:
        word_info = search_word.group("content")
        ids = compl_id_re.findall(word_info)
        if ids:
            if word_or_phrase == "word":
                link_word = "https://ru.forvo.com/download/mp3/{word}/ru/{id}".format(word=name_file, id=ids[0])
            else:
                link_word = "https://ru.forvo.com/download/phrase/mp3/{word}/ru/{id}".format(word=name_file, id=ids[0])
            response_data = session.request(method="GET", url=link_word)
            response_content = response_data.content

            with open(path_create_rus_file, "wb") as f:
                f.write(response_content)
            time.sleep(1)
            is_created = True
        else:
            print("\nНе найден контент - %s, для %s" % (word_search, word))
            error_list[name_file] = word_i
            is_created = False
    else:
        print("\nНе найдено - %s, для %s\n%s" % (word_search, word, url_word))
        error_list[name_file] = word_i
        is_created = False
    return is_created


for i, word_i in enumerate(list_word):
    #time.sleep(1)
    try:
        word, transl, transk = word_i.split(";")
        transl_list = transl.split(",")
        word_search = get_word(transl_list)
    except Exception as e:
        print("\nПроблема - %s, для %s" % (word_i, i+1))
        print(e)

    word_or_phrase = "word"
    name_file = word_search
    if len(word_search.split(" ")) > 1:
        word_or_phrase = "phrase"
        name_file = word_search.replace(" ", "_")

    is_created = create_sound_file(word_or_phrase, name_file)
    if not is_created and word_or_phrase == "phrase":
        # если искали фразу и не нашли - поищем среди слов
        is_created = create_sound_file("word", name_file)




    # temp_url = "https://ru.forvo.com/{word_or_phrase}/{content}/#ru"
    # url_word = temp_url.format(word_or_phrase=word_or_phrase, content=name_file)  # "phrase"
    #
    # path_create_rus_file = os.path.join(dir_rus_word, "%s_rus.mp3" % name_file)
    # if os.path.isfile(path_create_rus_file):
    #     continue
    # response_data = session.request(method="GET", url=url_word)
    # contant = response_data.content
    #
    # if word_or_phrase == "word":
    #     search_word = compl_parent_re_word.search(contant.decode())
    # else:
    #     search_word = compl_parent_re_phrase.search(contant.decode())
    #
    # if search_word:
    #     word_info = search_word.group("content")
    #     ids = compl_id_re.findall(word_info)
    #     if ids:
    #         if word_or_phrase == "word":
    #             link_word = "https://ru.forvo.com/download/mp3/{word}/ru/{id}".format(word=name_file, id=ids[0])
    #         else:
    #             link_word = "https://ru.forvo.com/download/phrase/mp3/{word}/ru/{id}".format(word=name_file, id=ids[0])
    #         # "https://ru.forvo.com/download/phrase/mp3/{word}/ru/{id}".format(word=word_search, id=ids[0])
    #         # session.headers.update({"Refere": "https://ru.forvo.com/word/{word}/".format(word=word_search)})
    #
    #         response_data = session.request(method="GET", url=link_word)
    #         response_content = response_data.content
    #
    #         with open(path_create_rus_file, "wb") as f:
    #             f.write(response_content)
    #         time.sleep(1)
    #     else:
    #         print("\nНе найден контент - %s, для %s" % (word_search, word))
    #         error_list.append(word_i)
    # else:
    #     print("\nНе найдено - %s, для %s\n%s\n" % (word_search, word, url_word))
    #     error_list.append(word_i)


#####################################################################################
link_word = "https://ru.forvo.com/download/mp3/film/en/598445"
session.headers.update({"Refere": "https://ru.forvo.com/word/film/"})
response_data = session.request(method="GET", url=link_word)
response_content = response_data.content
with open("2.mp3", "wb") as f:
    f.write(response_content)
print()
#session.cookies.set('sid', sid, domain=self.host, path='/')