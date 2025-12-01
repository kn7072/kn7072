import json
import os
import re
from string import Template

from config import (
    comment_block,
    compl_mnemo,
    container_block,
    dir_for_search_files,
    path_anki,
    path_dir,
    path_file_not_learn,
    path_synonyms_dir,
    pattern_examples,
    pattern_mnemo_galagoliy,
    pattern_search_word_in_text,
    star_comment_block,
    word_block,
)


def parse_file(word_i):  # , send_examples=False, send_mes=True
    word_i_lower = word_i.lower()
    path_file = os.path.join(path_dir, f"{word_i_lower}.txt")
    temp_list_msg = ["|-|", ["-"], ["-"], ""]
    try:
        with open(path_file, encoding="utf-8") as f:
            first_line = f.readline()
            temp_list_msg[0] = first_line
            # send_message_from_bot(first_line)
            print(first_line)
            next_data_file = f.read()

            search_mnemo = compl_mnemo.search(next_data_file)
            mnemo_text = []
            if search_mnemo:
                mnemo_text = search_mnemo.group("mnemo")
                print(mnemo_text)
                print("#" * 30)
                mnemo_text = mnemo_text.replace("\xa0", "")
                mnemo_text = [i for i in mnemo_text.split("\n") if i]
                # send_message_from_bot(mnemo_text)
            temp_list_msg[1] = mnemo_text
            # if send_examples:
            search_examples = re.findall(
                pattern_examples, next_data_file, flags=re.DOTALL | re.MULTILINE
            )
            if search_examples:
                # msg = "\n".join(search_examples)
                examples = [
                    i.replace("\n", "").replace("+", "").replace("#", "")
                    for i in search_examples
                ]  # msg
                # send_message_from_bot(msg)
            else:
                examples = [
                    i.replace("\xa0", "") for i in next_data_file.split("\n") if i
                ]
                # send_message_from_bot(next_data_file)
            # else:

            temp_list_msg[2] = examples

    except Exception as e:
        print(e)
        temp_list_msg[3] = str(e)
    else:
        temp_list_msg[3] = ""

    # if send_mes:
    #     send_message_list(temp_list_msg)
    return temp_list_msg


def prepare_garibjan():
    import re

    temp_dict = {}
    parrern = r"(?P<num>\d{1,4})\.\s+?(?P<word>[\w]+?)\s+?\[(?P<sound>[\w\'\(\)\:]+?)\]\s+?(?P<trans>.+?)"
    regex = re.compile(parrern)
    path_file = os.path.join(path_anki, "Мнемоника", "Гарибян.txt")
    for i in open(path_file, encoding="utf-8"):
        i = i.replace("\n", "").replace("\t", "").replace("\xad", "")
        # найти строки в которых неслько раз встречаются "-"
        try:
            info_word, mnemo = i.split("-", 1)
            search = regex.search(info_word)
            if search:
                temp_dict[search.group("word")] = (
                    i.replace(f"{search.group('num')}.", "").replace(";", ".").strip()
                )  # i
            else:
                # print(f"Что-то пошло не так с {i}")
                # print()
                pass
        except Exception as e:
            print(e, i)
    return temp_dict


def prepare_galagoliya():
    path_file = os.path.join(path_anki, "Мнемоника", "Голаголия.txt")
    temp_list = []
    for i in open(path_file, encoding="utf-8"):
        if i.startswith("***"):
            temp_list.append([])
            continue
        else:
            i_prepare = i.replace("\n", "").strip()
            if i_prepare:
                temp_list[-1].append(i_prepare)
    return temp_list


def get_data_file(path_file):
    with open(path_file, encoding="utf-8") as f:
        return f.read()


def get_mnemo_galagoliya(word):
    list_temp = []
    pattern_word = pattern_mnemo_galagoliy % word
    compl_mnemo_galagoliy = re.compile(pattern_word, flags=re.DOTALL | re.MULTILINE)
    for i in mnemo_galagoliya:
        block_i = "\n".join(i)
        search = compl_mnemo_galagoliy.search(block_i)
        if search:
            list_temp.append(block_i)
    return list_temp


def get_synonyms_html(word):
    pattern = pattern_search_word_in_text % word
    compl_pattern = re.compile(pattern, flags=re.DOTALL | re.MULTILINE)
    synonyms = dict_synonyms.get(word)
    synonyms_translate_html = None
    separate_synonyms = "-" * 15
    template_html_to_replace = f"<span class='found_word'>{word}</span>"

    if not word:
        return synonyms_translate_html

    def search_word():
        """Ищем слово в тексте, на случай если слово не является ключом в
        dict_synonyms, но присутствует к списках синонемов"""
        searche_dict = {}
        for word_i, val_i in dict_synonyms.items():
            for translate_i in val_i["translate"]:
                search = compl_pattern.search(translate_i)
                if search:
                    find_word = searche_dict.get(word_i)
                    if not find_word:
                        searche_dict[word_i] = {}
                        searche_dict[word_i]["translate"] = []
                    searche_dict[word_i]["translate"].append(translate_i)
        return searche_dict

    def create_html(word, synonyms):
        temp = []
        for translate_i in synonyms["translate"]:
            macmillan_stars, macmillan_ipa = get_ipa_and_stars_macmillan(word)

            html_stars = "".join(
                [f"<span class='star-mini'></span>" for i in range(macmillan_stars)]
            )
            translate_i = f"""<span class='synonym'>{word}</span><span class='ipa-margin'>{macmillan_ipa}</span>{html_stars} {translate_i}"""
            temp_translate = "".join(
                [f"<div>{i}</div>" for i in translate_i.split("\n") if i]
            )
            temp.append(temp_translate)
        synonyms_translate = f"<div>{separate_synonyms}</div>".join(temp)
        return synonyms_translate

    def replace_word_to_html(dict_translate):
        """Заменяем искомое слово (word) на шаблон, чтобы подсветить в тексте"""
        temp = []
        for text_i in dict_translate["translate"]:
            temp_text = text_i.replace(word, template_html_to_replace)
            temp.append(temp_text)
        return {"translate": temp}

    if synonyms:
        synonyms_translate_html = create_html(word, synonyms)
    else:
        synonyms = search_word()
        if synonyms:
            temp_list_html = []
            for word_i, translate_list_i in synonyms.items():
                translate_replaced = replace_word_to_html(translate_list_i)
                html_word_i = create_html(word_i, translate_replaced)
                temp_list_html.append(html_word_i)
            synonyms_translate_html = f"<div>{separate_synonyms}</div>".join(
                temp_list_html
            )

    return synonyms_translate_html


def get_sipmle_synonyms_html(word):
    synonyms = dict_synonyms.get(word)
    synonyms_translate_html = ""
    separate_synonyms = "-" * 15

    if not word:
        return synonyms_translate_html

    def create_html(synonyms):
        temp = []
        for translate_i in synonyms["translate"]:
            temp_translate = "".join(
                [f"<div>{i}</div>" for i in translate_i.split("\n") if i]
            )
            temp.append(temp_translate)
        synonyms_translate = f"<div class='payload'>{separate_synonyms}</div>".join(
            temp
        )
        synonyms_translate = comment_block.format(
            title_block="Синонимы", content_block="".join(temp)
        )
        return synonyms_translate.replace("\n", "")

    if synonyms:
        synonyms_translate_html = create_html(synonyms)

    return synonyms_translate_html


def get_html_for_synonyms_and_building(word, translate, add_html_code=""):
    """
    Возвращает верстку для синонимов и словообразования
    """
    macmillan_stars, macmillan_ipa = get_ipa_and_stars_macmillan(word)
    html_stars = "".join(
        [f"<span class='star-mini'></span>" for i in range(macmillan_stars)]
    )
    word_html = f"""<div onclick='myClick(this)'>
                        <span class="synonym">{word}</span>
                        <span class='ipa-margin'>{macmillan_ipa}</span>
                        {html_stars}
                        <span>{translate}</span>
                        
                        {add_html_code}
                    </div>"""
    return word_html


def get_ipa_and_stars_macmillan(word):
    """
    Возвращает число звезд и ipa
    """
    word_with_first_upper_symbol = ""
    if word:
        word_with_first_upper_symbol = word[0].upper() + (
            word[1:] if len(word) > 1 else ""
        )

    info_word = dict_macmillan.get(word) or dict_macmillan.get(
        word_with_first_upper_symbol
    )
    count_stars = 0
    ipa = "|-|"
    if info_word:
        count_stars = info_word["stars"]
        ipa = f"| {info_word['ipa']} |"
    return count_stars, ipa


def get_comment_word(word):
    """
    Возвращает комментарий к слову
    """
    temp = []
    if not word:
        return temp

    first_symbol = word[0].lower()  # слова сгруппированы по первый буквам
    path_to_file = os.path.join(path_anki, "WORDS", first_symbol, f"{word}.json")
    if os.path.isfile(path_to_file):
        data_file = json.loads(get_data_file(path_to_file))
        data_word = data_file[
            list(data_file)[0]
        ]  # в data_file только один ключ(слово),
        # так не известно в каком регистре будет слово сделал  data_file[list(data_file)[0]] всесто data_file.get(word)
        if data_word:
            return data_word["comment"]
        else:
            # если не нашли слово, возможно слово начинается с нижнего регистра
            data_word = data_file.get(first_symbol + word[1:])
            if data_word:
                return data_word["comment"]
    else:
        return temp


def get_html_comment_word(word):
    comment_list = get_comment_word(word)
    temp_html_comment = "<div>%s</div>"
    html_temp = """
                    <div class="hidden content">
                        {html}
                    </div>
                """

    comment_html = []
    if comment_list:
        temp_html_comment = "".join([temp_html_comment % i for i in comment_list])
        for comment_i in comment_list:
            first_line, mnemo_list, examples_str, error = parse_file(comment_i)
            word_i = transcription = translate = mnemo_html = html_trans_mnemo = ""
            if first_line != "|-|":
                tmp_list = [i.strip() for i in first_line.split("|")]
                if len(tmp_list) == 3:
                    word_i, transcription, translate = tmp_list
                if not mnemo_list:
                    mnemo_list = get_mnemo_list(comment_i)
                mnemo_html = (
                    "\n".join([f"<div>{i}</div>" for i in mnemo_list])
                    if mnemo_list
                    else ""
                )
                if word_i or mnemo_html:
                    html = f"<div>{translate}</div><div></div>{mnemo_html}"
                    html_trans_mnemo = html_temp.format(html=html)

            info_word = get_html_for_synonyms_and_building(
                comment_i, "", html_trans_mnemo
            )

            comment_html.append(info_word)
        comment_html = "".join(comment_html)
    return comment_html


def get_html_word(word, ipa, translate, mnemo_list, examples_list):
    synonyms = get_synonyms_html(word)
    # synonyms_linvinov = get_synonyms_linvinov_html(word)
    # word_building = get_word_building_linvinov_html(word)

    mnemo_html = ""
    if mnemo_list:
        prepare_mnemo = [i.split("\n") for i in mnemo_list]
        temp_list_mnemo = []
        for list_i in prepare_mnemo:
            mnemo_i = "\n".join([f"<div>{i}</div>" for i in list_i])
            temp_list_mnemo.append(mnemo_i)
        mnemo_html = "<div>-----</div>".join(temp_list_mnemo)
    examples_html = (
        "\n".join([f"<div>{i}</div><div>-----</div>" for i in examples_list])
        if examples_list
        else ""
    )
    macmillan_stars, _ = get_ipa_and_stars_macmillan(word)
    word_comment_html = get_html_comment_word(word)

    base_html = """
            <div class="container-word">
                        <div class="word_en">
                            <div class="wrap_word">
                                <div class="content
                                            mrg_right-10
                                            pointer"
                                    onmouseenter='mouseHoverWord(this)'
                                    onmouseleave='mouseHoverWord(this)'>
                                    {word}
                                </div>
                                <div class="hidden content">
                                    {ipa}
                                </div>
                            </div>
                            
                            <div class="wrap_delete">
                                <input class="mrg_right-10 
                                            checkbox-delete" type="checkbox" id={word} name={word}>
                                <input type="button" value="Удалить" class="delete" 
                                    onclick='deleteWord(this, "{word}")'/>
                            {stars}
                            </div>
                        </div>
                        <div class="sound" 
                            onclick='listen(this, "{word}")'>Озвучить</div>
                        <div class="translate clickable" 
                            onclick='myClick(this)'>Перевод
                            <div class="hidden content">
                                {translate}
                            </div>
                        </div>
                        {mnemo_temp}
                        {synonyms_temp}
                        {synonyms_litvinov_temp}
                        {word_duilding_temp}
                        {word_comment_temp}
                        {examples_temp}
                    </div>
            """
    mnemo_temp = """
    <div class="memorize clickable" 
                            onclick='myClick(this)'>Мнемоника
                            <div class="hidden content">
                                {mnemo}
                            </div>
                        </div>
    """
    synonyms_temp = """
    <div class="memorize clickable" 
                            onclick='myClick(this)'>Синонимы
                            <div class="hidden content">
                                {synonyms}
                            </div>
                        </div>
    """
    synonyms_litvinov_temp = """
    <div class="memorize clickable" 
                            onclick='myClick(this)'>Синонимы_Литвинов
                            <div class="hidden content">
                                {synonyms_linvinov}
                            </div>
                        </div>
    """
    word_duilding_temp = """
    <div class="memorize clickable" 
                            onclick='myClick(this)'>Словообразование
                            <div class="hidden content">
                                {word_building}
                            </div>
                        </div>
    """
    examples_temp = """
    <div class="examples clickable" 
                            onclick='myClick(this)'>Примеры
                            <div class="hidden content">
                                {examples}
                            </div>
                        </div>
    """

    star_tmp = """<div class="star"></div>"""
    word_comment_temp = """<div class="memorize clickable" 
                            onclick='myClick(this)'>Комментарий
                            <div class="hidden content">
                                {word_comment}
                            </div>
                        </div>
    """

    mnemo_temp = mnemo_temp.format(mnemo=mnemo_html) if mnemo_html else ""
    synonyms_temp = synonyms_temp.format(synonyms=synonyms) if synonyms else ""
    word_duilding_temp = (
        word_duilding_temp.format(word_building=word_building) if word_building else ""
    )
    examples_temp = (
        examples_temp.format(examples=examples_html) if examples_html else ""
    )
    stars_html = "".join([star_tmp for _ in range(macmillan_stars)])
    word_comment_temp = (
        word_comment_temp.format(word_comment=word_comment_html)
        if word_comment_html
        else ""
    )

    return base_html.format(
        word=word,
        ipa=ipa,
        stars=stars_html,
        translate=translate,
        mnemo_temp=mnemo_temp,
        synonyms_temp=synonyms_temp,
        synonyms_litvinov_temp=synonyms_litvinov_temp,
        word_duilding_temp=word_duilding_temp,
        word_comment_temp=word_comment_temp,
        examples_temp=examples_temp,
    )


def read_file(path_file):
    """
    Возврщает список слов для изучения
    """
    list_word = []
    for i in open(path_file, mode="r", encoding="utf-8"):
        list_word.append(i.split(";")[0].strip())
    return list_word


def create_file(path_file: str, bin_data: bin):
    """Создает файл."""
    with open(path_file, mode="bw") as f:
        f.write(bin_data)


def get_mnemo_list(word):
    mnemo_list_tmp = []
    mnemo_list = []
    mnemo_garibjan_word = mnemo_garibjan.get(word, "")
    if mnemo_garibjan_word:
        mnemo_list_tmp.append(mnemo_garibjan_word)
    mnemo_list_tmp.extend(get_mnemo_galagoliya(word))  # mnemo_galagoliya

    for mnemo_i in mnemo_list_tmp:
        mnemo_i = mnemo_i.replace("\xa0", "")
        mnemo_list.extend([i for i in mnemo_i.split("\n") if i])
        mnemo_list.append("####")

    if mnemo_list:
        # чтобы убрать последние "####"
        mnemo_list = mnemo_list[0:-1]

    return mnemo_list


def not_learn_word(word):
    with open(path_file_not_learn, encoding="utf-8", mode="a") as f:
        f.write(word + "\n")


def get_path_file(word: str) -> str:
    """Возвращает путь до файла."""
    first_symbol = word[0].lower()
    path_file = ""
    path_file_temp = os.path.join(
        dir_for_search_files, first_symbol, word.lower() + ".json"
    )
    if os.path.isfile(path_file_temp):
        path_file = path_file_temp
    else:
        print(f"Нет файла {path_file_temp}")
    return path_file


def get_html_mnemonic(mnemo_list):
    tmp_html_list = []
    for mnemo_i in mnemo_list:
        html_mnemo_i = "".join([f"<div>{i}</div>" for i in mnemo_i.split("\n")])
        tmp_html_list.append(html_mnemo_i)
    return "<div></div>".join(tmp_html_list)


def get_html_comments(words_list):
    list_html_comments = []
    for word_i in words_list:
        try:
            path_word_i = get_path_file(word_i)
            data_file_i = get_data_file(path_word_i)
            data_file_i_json = json.loads(data_file_i)
            word_key = list(data_file_i_json.keys())[0]
            data_word = data_file_i_json[word_key]
            count_stars = data_word["stars"]
            stars_block = container_block.format(
                content=star_comment_block * count_stars
            )
            content_block = f"<div>{data_word['translate']}</div>" + get_html_mnemonic(
                data_word["mnemonic"]
            )
            word_block_html = word_block.format(
                word=word_i, ipa=data_word["transcription"], stars_block=stars_block
            )
            comment_html = comment_block.format(
                title_block=word_block_html, content_block=content_block
            ).replace("\n", "")
            list_html_comments.append(comment_html)
        except Exception as e:
            print(e)
            print(word_i)
    return list_html_comments


mnemo_garibjan = prepare_garibjan()
mnemo_galagoliya = prepare_galagoliya()

path_to_json_synonyms = os.path.join(path_synonyms_dir, "words.json")
dict_synonyms = json.loads(get_data_file(path_to_json_synonyms))
