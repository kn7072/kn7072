# coding="utf-8"
import requests
import os
import re
temp_1 = "id=\"audio_us\"(?P<text>.+)id=\"audio_uk\""
temp_1 = "id=\"us_tr_sound\"(?P<text>.+)id=\"uk_tr_sound\""
compl_1 = re.compile(temp_1)

temp_2 = "src=\"(?P<path_sound>.*?.mp3)\""
compl_2 = re.compile(temp_2)

temp_trans = "transcription\">(?P<trans>.*?)<"
compl_trans = re.compile(temp_trans)

def get_sound():
    pass

list_ind = []


def get_index_list(text, sub_str, ind):
    try:
        ind_temp = text.index(sub_str, ind)
        list_ind.append(ind_temp)
        get_index_list(text, sub_str, ind_temp+1)
    except ValueError:
        return
    return

# get_index_list(data_html, "body", 0)
# temp_test = data_html[1193:44065]
# tree = etree.fromstring(temp_test)
# xpathData = tree.xpath('div#wd')
def create_sound_file(name, data_file, path_dir):
    path_to_file = os.path.join(path_dir, "%s.mp3" % name)
    with open(path_to_file, mode="wb") as f:
        f.write(data_file)

url = "https://wooordhunt.ru"
word_name = "Champagne"
url_word = "%s/word/%s" % (url, word_name)

url_word = "https://translate.google.com/?hl=en&tab=TT&sl=en&tl=ru&text=clergyman&op=translate"
r = requests.get(url_word)
data_html = r.text
with open('TEMP.html', encoding="utf-8", mode='w') as f:
    f.write(data_html)


search = compl_1.search(data_html)
all_test = search.group("text")

search_sound = compl_2.search(all_test)
paht_to_sound = search_sound.group("path_sound")
all_path = url + paht_to_sound
data_sound = requests.get(all_path)
path_dir_sounds = os.path.join(os.getcwd(), "audio")
create_sound_file(word_name, data_sound.content, path_dir_sounds)

search_trans_text = compl_trans.search(all_test)
trans_text = search_trans_text.group("trans")
print(trans_text)

