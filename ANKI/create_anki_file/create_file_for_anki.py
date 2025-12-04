import json
import os

from common import (
    get_data_file,
    get_html_comments,
    get_html_mnemonic,
    get_path_file,
    get_sipmle_synonyms_html,
    read_file,
)
from config import (
    comment_block,
    comment_header_block,
    div_block,
    path_dir_sound_files,
    path_to_all_words,
    path_to_learnt_sentence,
    star_span_block,
)

path_anki_to_create = "/home/stepan/temp/anki/{i}_English_words.txt"

data_all_words = read_file(path_to_all_words)  # ALL_WORDS.txt ПОВТОРИТЬ.txt

delimeter = ";"
ccs_class_even = "even"
css_class_odd = "odd"

"""
https://docs.ankiweb.net/searching.html

deck:My\_English\_words\_base

deck:My\_English\_words\_base::en-ru
deck:My\_English\_words\_base::ru-en
deck:My\_English\_words\_base::type-en

card:орфография
card:англ-рус
card:рус-англ


card:англ-рус "deck:По умолчанию"
card:рус-англ "deck:По умолчанию"
card:орфография "deck:По умолчанию"
"""


def get_eng_examples(list_examples):
    """
    Возвращает верстку для передней стороны карточки - только примеры на английском(без перевода)
    :param list_examples:
    :return:
    """
    temp_list = []
    temp_html = "<div class='%s'>%s</div>"
    for ind, val_i in enumerate(list_examples):
        if ind % 2 != 0:
            temp_list.append(temp_html % (ccs_class_even, val_i))
        else:
            temp_list.append(temp_html % (css_class_odd, val_i))

    # убераю из последнего элемента #
    temp_list[-1] = temp_list[-1].replace("#", "")
    examples = "".join(temp_list)
    return examples


def get_learnt_sentence() -> dict:
    """
    Возвращает словать предложений которые уже в списке на изучение
    """
    temp_dict = {}
    for line_i in open(path_to_learnt_sentence, encoding="utf-8"):
        words, eng, rus = line_i.split(";")
        eng = eng.strip()
        if temp_dict.get(eng):
            continue
        else:
            temp_dict[eng] = words

    return temp_dict


def get_eng_rus_examples(list_examples_eng, list_examples_rus):
    """
    Возвращает верстку для ОБОРОТНОЙ стороны карточки - примеры с переводом
    :param list_examples_eng:
    :param list_examples_rus:
    :return:
    """
    temp_list = []
    temp_html = """
    <div class="phrase padding-container {odd_even} {is_learnt_class}">
        <p>{eng}</p>
        <p class="payload">{rus}</p>
    </div>
    """
    join_examples = zip(list_examples_eng, list_examples_rus)

    for ind, val_i in enumerate(join_examples):
        # если предложение найдено в learnt_sentence - помечаем его классом ouline-checbox
        is_learn = 0
        is_learnt_class = ""
        if learnt_sentence.get(val_i[0]):
            is_learnt_class = "outline-container"
            is_learn = 1

        eng = val_i[0]
        rus = val_i[1]
        if "'" in eng:
            # экранирование апострофа
            eng = eng.replace("'", "\\'")

        temp_list.append((is_learn, is_learnt_class, eng, rus))

    temp_list.sort(key=lambda x: x[0], reverse=True)
    examples_list = []
    for ind, val_i in enumerate(temp_list):
        is_learnt_class = val_i[1]
        eng = val_i[2]
        rus = val_i[3]
        odd_even = ccs_class_even

        if ind % 2 == 0:
            odd_even = css_class_odd
        examples_list.append(
            temp_html.format(
                odd_even=odd_even,
                is_learnt_class=is_learnt_class,
                eng=eng,
                rus=rus,
            ),
        )

    examples = "".join(examples_list).replace("\n", "")
    return examples


list_exists_mnemo = []
error_list = []


def get_content_word(data_all_words):
    for word_i in data_all_words:
        # word_i = 'brown'
        path_word_i = get_path_file(word_i)
        if path_word_i:
            data_file_i = get_data_file(path_word_i)
            data_file_i_json = json.loads(data_file_i)
            word_key = list(data_file_i_json.keys())[0]
            data_word = data_file_i_json[word_key]

            sound_word_i = f"[sound:{word_i}.mp3]"
            path_sound = os.path.join(path_dir_sound_files, "%s.mp3" % word_i)
            if not os.path.isfile(path_sound):
                print(path_sound)

            mnemonic = ""
            examples = ""
            example_translate = ""
            comments = ""
            data_mnemonic = data_word["mnemonic"]
            data_examples = data_word["examples"]
            data_example_translate = data_word["example_translate"]
            data_comments = data_word["comment"]
            if data_mnemonic:
                mnemonic = comment_block.format(
                    title_block="Мнемоника",
                    content_block=get_html_mnemonic(data_mnemonic),
                ).replace("\n", "")
                mnemonic = f"<br>{mnemonic}"
            if data_examples:
                examples = get_eng_examples(data_examples)
            if data_comments:
                comments = "".join(get_html_comments(data_comments))
                header_block = comment_header_block.format(content_block="Комментарии")
                comments = f"<br>{header_block}{comments}".replace("\n", "")

            count_stars = data_word["stars"]
            stars_block = div_block.format(content=star_span_block * count_stars)
            try:
                if data_example_translate and data_examples:
                    example_translate = get_eng_rus_examples(
                        data_examples, data_example_translate
                    )
            except Exception:
                print(word_i)

            synonyms = get_sipmle_synonyms_html(word_i)
            str_word = (
                "{translate}{delimeter}"
                "{word_i}{delimeter}"
                "{transcription}{delimeter}"
                "{sound_word}{delimeter}"
                "{mnemonic}{delimeter}"
                "{examples}{delimeter}"
                "{example_translate}{delimeter}"
                "{comments}{delimeter}"
                "{stars}{delimeter}"
                "{synonyms}\n".format(
                    translate=data_word["translate"],
                    word_i=word_i,
                    transcription=data_word["transcription"],
                    sound_word=sound_word_i,
                    mnemonic=mnemonic,
                    delimeter=delimeter,
                    examples=examples,
                    example_translate=example_translate,
                    comments=comments,
                    stars=stars_block,
                    synonyms=synonyms,
                )
            )
        yield str_word


content_iterator = get_content_word(data_all_words)
limit = 2000
i = 1
learnt_sentence: dict = get_learnt_sentence()

### ВРЕММЕННО - ДЛЯ ЗАПОЛЕНИНИЯ НЕДОСТАЮЩИХ ПРЕДЛОЖЕНИЙ
# limit = 230
# def temp_content():
#     list_word_learn = []
#     for line_i in open("/home/stepan/GIT/kn7072/GO/english/ADD_SENTENCE.txt", encoding="utf-8"):
#         word_i, frequency_i, *x = line_i.rsplit(" ", 1)
#         if x:
#             print(line_i)
#         list_word_learn.append(word_i)

#     return list_word_learn

# content_iterator = get_content_word(temp_content())
# ###


while True:
    path_to_create_anki_file = path_anki_to_create.format(i=i)
    with open(path_to_create_anki_file, "w", encoding="utf-8") as f:
        for num, word_content_i in enumerate(content_iterator, 1):
            # if "" in word_content_i:
            #     print()
            if len(word_content_i) > 131072:
                list_fields = word_content_i.split("&")
                for fild_i in list_fields:
                    print(len(fild_i))
            f.write(word_content_i)
            if num > limit:
                i += 1
                break
        else:
            break

# шаблон лица
"""
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css">
{{англ}}
<br>
{{транскрипция}}
<br>
{{звезды}}
<div style='font-family: Arial; font-size: 20px;'>{{озвучка_англ}}</div>
<br>
{{мнемоника}}
<br>
Комментарии
{{комментарии}}
<br>
{{пример}}
"""

# шаблон оборота
"""
<script>

function sendSentence(e, sentence) {
        var classList = e.classList;
        classList.add('red');
				  classList.remove('pointer');
					e.blur();
        send(sentence, 'sentence');
}

function checkedWord(e) {
	var parent = e.parentElement;
	var derive = parent.getElementsByClassName('learn')[0];
 var classes = derive.classList;

	if(e.checked) {
		derive.disabled = false;
		classes.add('pointer');
	} else {
		derive.disabled = true;
   classes.remove('pointer');
	}
}

function send(word, command) {
        var data = {
            word: word
        };

        var boundary = String(Math.random()).slice(2);
        var boundaryMiddle = '--' + boundary + '\r\n';
        var boundaryLast = '--' + boundary + '--\r\n'

        var body = ['\r\n'];
        for (var key in data) {
        // добавление поля
        body.push('Content-Disposition: form-data; name="' + key + '"\r\n\r\n' + data[key] + '\r\n');
        }

        body = body.join(boundaryMiddle) + boundaryLast;

        // Тело запроса готово, отправляем
        var xhr = new XMLHttpRequest();
        
        ip_address = "http://192.168.1.57"
        socket = `${ip_address}:8090`
        //socket = "http://localhost:8090"
        request_path = `${socket}/${command}`
        
        xhr.open("POST", request_path, true );
        // xhr.open("POST", "http://localhost:8088"+ "/sound", true );

        xhr.setRequestHeader('Content-Type', 'multipart/form-data; boundary=' + boundary);

        xhr.onreadystatechange = function() {
        if (this.readyState != 4) return;
        console.log( this.responseText );
        }

        xhr.send(body);
    }


</script>

{{рус}}
<br>
<br>
{{транскрипция}}
<div style='font-family: Arial; font-size: 20px;'>{{озвучка_англ}}</div>
<br>
<br>
{{мнемоника}}
<hr>
{{перевод_примеров}}
"""

# таблица стилей
"""
p {margin: 0 0 5px 0;}

.wrap_delete {
        display: flex;
        align-items: center;
    }
.star::after {
        content: "\f005";
        font-family: awesome;
        font-family: FontAwesome;
        color: red;
        margin-left: 5px;
}

.card {
 font-family: arial;
 font-size: 20px;
 text-align: center;
 color: black;
 background-color: white;
}
.phrase {
            background: #f2fbe7;
            border: 1px solid #dff5c4;
            border-radius: 6px;
            color: #000
        }
        .phrase:hover {
            background: #dff5c4;
            border: 1px solid gray;
            color: #000;
            cursor: pointer;
        }
        .phrase .payload {
            display: none;
        }

        .show .payload {
            display: block;
        }
        .phrase:hover > p  {
           display: block;
        }

 .phrase:hover > div  {
           display: block;
        }

.odd  {   background-color: #ebffe3;}
.even  {   background-color: #fff;}
.pointer {cursor: pointer;}
.red {outline: 2px solid red;}
.bottom-learn { margin-bottom: 10px; }
.mrg-right-15 { margin-right: 15px; }
.ouline-checbox { outline: 3px solid green; }
"""
