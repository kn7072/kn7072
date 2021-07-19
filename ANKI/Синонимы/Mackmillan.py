#coding:utf-8
import requests
import os
import json
import re
import time

path_to_save_content = "MackmillanHTML"
path_to_save_content_british = "MackmillanHTMLBritish"

pron_pattern = re.compile(r'\"PRON\".*?/\s*?\</span>(?P<pron>[\w\W]*?)<span', re.M|re.I)
red_star_pattern = re.compile("entry-red-star", re.M|re.I)
list_error_words = []
words_dict = {}

def create_json_file(name_file, data_file):
    with open(name_file, encoding="utf-8", mode="w") as f:
        for i in data_file:
            f.write(i)


def create_file(word, content, dir_to_save=path_to_save_content):
    path_to_save = os.path.join(dir_to_save, word + ".html")
    with open(path_to_save, mode="bw") as f:
        f.write(content)

def get_content(word, dictionary_version="american"):
    """
    dictionary_version может принимать одно из значений: american или british
    """
    time.sleep(1)
    print(word)
    link = f"https://www.macmillandictionary.com/us/dictionary/{dictionary_version}/{word}"
    headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
    data_word = None
    try:
        data_word = requests.get(link, headers=headers).content
    except: 
        list_error_words.append(word)
    return data_word

error_pron = []  # для ошибок транскрипции
error_stars = [] # для ошибок звезд

def parse_html(path_file):
    word = path_file.split("/")[-1].split(".")[0]
    

    with open(path_file, encoding="utf-8") as f:
        data_file = f.read()
        result_pron = pron_pattern.search(data_file)
        
        words_dict[word] = {"ipa": "", "stars": 0}
        if result_pron:
            pron = result_pron.group("pron")
            words_dict[word]["ipa"] = pron
        else:
            error_pron.append(word)

        num_srars = red_star_pattern.findall(data_file)     
        num_srars = len(num_srars) if num_srars else 0

        if num_srars:
            words_dict[word]["stars"] = num_srars
        else:
            error_stars.append(word)
        

def get_list_word():
    temp = []
    for word_i in open("./macmillan7000word.list", encoding="utf-8"):
        temp.append(word_i.replace("\n", "").strip())
    return temp

def get_download_word(dir_to_save=path_to_save_content):
    temp = []
    for i in os.listdir(dir_to_save):
        temp.append(i.replace(".html", ""))
    return temp    

def get_contant(list_word_for_download, dir_to_save=path_to_save_content, dictionary_version="american"):
    list_download_word = get_download_word(dir_to_save=dir_to_save)
    
    for word_i in list_word_for_download:
        if word_i in list_download_word:
            continue
        content_word = get_content(word_i, dictionary_version=dictionary_version)
        if content_word:
            create_file(word_i, content_word, dir_to_save=dir_to_save)

# list_word = get_list_word()
# get_content(list_word)
# for i in list_error_words:
#     print(i)

for file_html_i in os.listdir(path_to_save_content):
    path_to_file_i = os.path.join(path_to_save_content, file_html_i)
    parse_html(path_to_file_i)

# ПЫТАЕМСЯ ВЫГРУЗИТЬ ФАЙЛЫ ДЛЯ british, чтобы получить звезды которых нет в american
get_contant(list_word_for_download=error_stars, dir_to_save=path_to_save_content_british, dictionary_version="british")

error_stars = []
error_pron = []
for file_html_i in os.listdir(path_to_save_content_british):
    path_to_file_i = os.path.join(path_to_save_content_british, file_html_i)
    parse_html(path_to_file_i)

if error_pron:
    print("ОШИБКИ ТРАНСКРИПЦИИ")
    for i in error_pron:
        print(i)

if error_stars:
    print("ОШИБКИ stars")
    for i in error_stars:
        print(i)   

print(len(words_dict.keys()))
data_json = json.dumps(words_dict, ensure_ascii=False, indent=4)

create_json_file("macmillan_ipa_stars.json", data_json)