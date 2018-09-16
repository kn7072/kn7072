# coding="utf-8"
import requests
import os
import re

temp_1 = "id=\"audio_us\"(?P<text>.+)id=\"audio_uk\""
temp_1 = "id=\"us_tr_sound\"(?P<text>.+)id=\"uk_tr_sound\""
compl_1 = re.compile(temp_1)

temp_sound = "src=\"(?P<path_sound>.*?.mp3)\""
compl_sound = re.compile(temp_sound)

temp_trans = "transcription\">(?P<transcription>.*?)<"
compl_trans = re.compile(temp_trans)

temp_translate = "t_inline_en\">(?P<translate>.+?)<"
compl_translate = re.compile(temp_translate)


def create_sound_file(name, data_file, path_dir):
    path_to_file = os.path.join(path_dir, "%s.mp3" % name)
    with open(path_to_file, mode="wb") as f:
        f.write(data_file)

url = "https://wooordhunt.ru"
word_name = "Champagne"


def get_info_word(word):
    url_word = "%s/word/%s" % (url, word)
    r = requests.get(url_word)
    data_html = r.text

    search = compl_1.search(data_html)
    all_test = search.group("text")

    search_sound = compl_sound.search(all_test)
    paht_to_sound = search_sound.group("path_sound")
    all_path = url + paht_to_sound
    data_sound = requests.get(all_path)
    path_dir_sounds = os.path.join(os.getcwd(), "audio")
    create_sound_file(word, data_sound.content, path_dir_sounds)

    search_transcription = compl_trans.search(all_test)
    transcription = search_transcription.group("transcription")

    search_translate = compl_translate.search(data_html)
    translate = search_translate.group("translate")
    return word, translate, transcription

if __name__ == "__main__":
    res = get_info_word("house")
    print(res)
    print()