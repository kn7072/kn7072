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
    """
    Возвращает верстку для передней стороны карточки - только примеры на английском(без перевода)
    :param list_examples:
    :return:
    """
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

def get_eng_rus_examples(list_examples_eng, list_examples_rus):
    """
    Возвращает верстку для ОБОРОТНОЙ стороны карточки - примеры с переводом
    :param list_examples_eng:
    :param list_examples_rus:
    :return:
    """
    temp_list = []
    temp_html = """<div class="phrase hidden %s"><p class="trigger">%s  #</p><p class="payload">%s  #</p></div>"""
    join_examples = zip(list_examples_eng, list_examples_rus)
    for ind, val_i in enumerate(join_examples):
        if ind % 2 != 0:
            temp_list.append(temp_html % (ccs_class_even, val_i[0], val_i[1]))
        else:
            temp_list.append(temp_html % (css_class_odd, val_i[0], val_i[1]))

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
                examples = get_eng_examples(value_i["examples"])
            try:
                if value_i["example_translate"] and value_i["examples"]:
                    example_translate = get_eng_rus_examples(value_i["examples"], value_i["example_translate"])

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

create_file(path_anki, data_json)
# ФАЙЛЫ НАХОДЯТСЯ C:\Users\Stepan1\AppData\Roaming\Anki2\1-й пользователь\collection.media
"""
https://lingvo2.ru/docs/anki/ankitest-manual.htm

англ:grea*


card:орфография
card:англ-рус
card:рус-англ


{{FrontSide}} - отображает переднюю карточку
"""
"""
ЛИЦЕВАЯ сторона
<a href="https://wooordhunt.ru/word/{{англ}}">{{англ}}</a>
<script>
   var phrase = document.getElementsByClassName('phrase');
   for (var index = 0; index < phrase.length; index++) {
    phrase[index].addEventListener('click', clickHandler);
}

function clickHandler(event) {
    event.preventDefault();
   this.classList.toggle('hidden');
}
</script>

<br>
{{транскрипция}}
<br>
<div style='font-family: Arial; font-size: 20px;'>{{озвучка_англ}}</div>
<br>
{{пример}}
#####################################################################################
СТИЛЬ

p {margin: 0 0 5px 0;}

.card {
 font-family: arial;
 font-size: 20px;
 text-align: center;
 color: black;
 background-color: white;
}

.phrase {background: #f2fbe7; border: 1px solid #dff5c4; border-radius: 6px; color: #000} .phrase.hidden:hover {background: #dff5c4; color: #000; cursor: pointer;}
.phrase.hidden .payload {display: none;}

.phrase.shown {background: #fff; color: #000;}
.phrase.shown .trigger {display: none;}
.phrase.shown .payload {display: block;}

.odd  {   background-color: #ebffe3;}
.even  {   background-color: #fff;}
#####################################################################################

ОБРАТНАЯ СТОРОНА

<script>
   var phrase = document.getElementsByClassName('phrase');
   for (var index = 0; index < phrase.length; index++) {
    phrase[index].addEventListener('click', clickHandler);
}

function clickHandler(event) {
    event.preventDefault();
   this.classList.toggle('hidden');
}
</script>

{{рус}}
<hr>
{{перевод_примеров}}
"""










