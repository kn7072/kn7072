# -*- coding: utf-8 -*-
import json
import os


path_to_json_file = "full_words.json"
path_anki = r"temp\My_English_words_3.txt"
path_dir_sound_files = "d:\kn7072\EnglishSimulate\Project\sound_longman"
delimeter = ";"
ccs_class_even = "even"
css_class_odd = "odd"

def get_eng_examples(list_examples):
    temp_list = []
    temp_html = "<div class='%s'>%s  #</div>"
    for ind, val_i in enumerate(list_examples):
        if ind % 2 != 0:
            temp_list.append(temp_html % (ccs_class_even, val_i))
        else:
            temp_list.append(temp_html % (css_class_odd, val_i))

    # убераю из последнего элемента #
    temp_list[-1] = temp_list[-1].replace("#", "")
    examples = "".join(temp_list)
    return examples

def create_file(path_anki, data_words):

    with open(path_anki, "w", encoding="utf-8") as f:
        for word_i, value_i in data_words.items():
            sound_word_i = "[sound:%s.mp3]" % word_i
            path_sound = os.path.join(path_dir_sound_files, "%s.mp3" % word_i)
            if not os.path.isfile(path_sound):
                print(path_sound)

            mnemonic = ""
            examples = ""
            example_translate = ""
            if value_i["mnemonic"]:
                mnemonic = " #".join(value_i["mnemonic"])
            if value_i["examples"]:
                examples = get_eng_examples(value_i) 
            try:
                if value_i["example_translate"]:
                    temp = ["<div>%s  #</div>" % i for i in value_i["example_translate"]]
                    # убераю из последнего элемента #
                    temp[-1] = temp[-1].replace("#", "")
                    example_translate = "".join(temp)

            except Exception:
                print(word_i)
            str_word = "{translate}{delimeter}" \
                       "{word_i}{delimeter}" \
                       "{transcription}{delimeter}" \
                       "{sound_word}{delimeter}" \
                       "{mnemonic}{delimeter}" \
                       "{examples}{delimeter}" \
                       "{example_translate}\n"\
                .format(translate=value_i["translate"],
                        word_i=word_i,
                        transcription=value_i["transcription"],
                        sound_word=sound_word_i,
                        mnemonic=mnemonic,
                        delimeter=delimeter,
                        examples=examples,
                        example_translate=example_translate)
            f.write(str_word)

with open(path_to_json_file, "r", encoding="utf-8") as f:
    data_json = json.loads(f.read())

# ФАЙЛЫ НАХОДЯТСЯ C:\Users\Stepan1\AppData\Roaming\Anki2\1-й пользователь\collection.media
"""
https://lingvo2.ru/docs/anki/ankitest-manual.htm

англ:grea*


card:орфография
card:англ-рус
card:рус-англ
"""
create_file(path_anki, data_json)








