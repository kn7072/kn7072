import config_bot
import requests
import os
import signal
from subprocess import Popen, PIPE
import re
import time
from config_bot import count_sound, path_dir_mp3, path_to_mplayer, time_sound_pause, path_dir, compl_mnemo,  \
    pattern_examples, schedule, path_anki, path_file_not_learn, separate, name_base, path_synonyms_dir,  \
    path_word_building_dir, pattern_search_word_in_text, path_to_save_reports, path_file_words, path_all_words
from datetime import datetime, timedelta
import datetime as dt
from db import into_table, fetchall, clear_table
import json
import traceback
import sys


def send_message_from_bot(text):
    for chat_id in config_bot.chat_id_list:
        req_message = f"https://api.telegram.org/bot{config_bot.token}/sendMessage?chat_id={chat_id}&text={text}"
        #  print(req_message)
        res = requests.get(req_message)


def play_sound(word, volume=0.8, count_sound=count_sound):
    """
    stream music with mixer.music module in a blocking manner
    this will stream the sound from disk while playing
    """
    import pygame as pg
    # path_file = 'audio/{word}.mp3'.format(word=word)
    path_file = os.path.normpath(os.path.join(path_dir_mp3, f"{word}.mp3"))
    # playsound.playsound('audio/{word}.mp3'.format(word=word), True)
    # set up the mixer
    freq = 44100  # audio CD quality
    bitsize = -16  # unsigned 16 bit
    channels = 2  # 1 is mono, 2 is stereo
    buffer = 2048  # number of samples (experiment to get best sound)
    pg.mixer.init(freq, bitsize, channels, buffer)
    # volume value 0.0 to 1.0
    pg.mixer.music.set_volume(volume)
    clock = pg.time.Clock()
    for _ in range(count_sound):
        try:
            pg.mixer.music.load(path_file)
            print("Music file {} loaded!".format(path_file))
        except pg.error:
            print("File {} not found! ({})".format(path_file, pg.get_error()))
            return
        pg.mixer.music.play()
        while pg.mixer.music.get_busy():
            # check if playback has finished
            clock.tick(30)
        time.sleep(time_sound_pause)


def sound(word, count_sound=count_sound):
    for _ in range(count_sound):
        try:
            path_sound_file = os.path.normpath(os.path.join(path_dir_mp3, f"{word}.mp3"))
            if not os.path.exists(path_sound_file):
                print(f"Не обнаружен файл {path_sound_file}")
            command_list = [path_to_mplayer,  path_sound_file]  #'-delay', '-%s' % time_sound_pause, '-loop', '2',
            command_str = " ".join(command_list)
            # print(f"Выполняется {command_str}")
            process = Popen(command_list, stdout=PIPE, stderr=PIPE)   #, stdout=subprocess.PIPE, stderr=subprocess.PIPE , shell=True, preexec_fn=os.setsid
            stdout, stderr = process.communicate(timeout=2)
        except Exception as e:
            # print(e, count_sound)
            os.kill(process.pid, signal.SIGTERM)
            return
        time.sleep(time_sound_pause)


def send_message_list(list_mes):
    for text_i in list_mes:
        if text_i:
            send_message_from_bot(text_i)    


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
            search_examples = re.findall(pattern_examples, next_data_file, flags=re.DOTALL | re.MULTILINE)
            if search_examples:
                # msg = "\n".join(search_examples)
                examples = [i.replace("\n", "").replace("+", "").replace("#", "") for i in search_examples]  # msg
                # send_message_from_bot(msg)
            else:
                examples = [i.replace("\xa0", "") for i in next_data_file.split("\n") if i]
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


def next_play():
    """
    Определяем - нужно ли продолжать озвучивать слова в зависимости от расписания
    """
    while True:
        currunt_day = datetime.combine(dt.date.today(), dt.time(00, 00, 00))
        current_time = datetime.now().timestamp()
        current_datetime = datetime.today()    
        current_day = current_datetime.strftime('%A')  
        schedule_day = schedule[current_day]
        
        for schedule_i in schedule_day:
            start_hour, start_minute = [int(i) for i in schedule_i["start"].split(":")]
            stop_hour, stop_minute = [int(i) for i in schedule_i["stop"].split(":")]
            
            t_start_delta = timedelta(hours=start_hour, minutes=start_minute)
            t_stop_delta = timedelta(hours=stop_hour, minutes=stop_minute)

            start_play = (currunt_day + t_start_delta).timestamp()
            stop_play = (currunt_day + t_stop_delta).timestamp()

            if start_play > stop_play:
                msg = msg = f"Значение ключа start должно быть меньше значеня ключа stop\n Day {current_day}\n schedule:\n{schedule_i}"
                raise Exception(msg)
            
            # x1 = current_time >= start_play
            # x2 = current_time <= stop_play
            # print(f"DEBUG current_time >= start_play {x1} and current_time <= stop_play  {x2}")
            
            
            if current_time >= start_play and current_time <= stop_play:
                return True

        time.sleep(60)  # чтобы не вызывать слишком часто


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
                temp_dict[search.group("word")] = i
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
    for i in mnemo_galagoliya:
        block_i = "\n".join(i)
        if word in block_i:
            list_temp.append(block_i)
    return list_temp 

def get_synonyms_html(word):
    
    pattern = pattern_search_word_in_text % word
    compl_pattern = re.compile(pattern, flags=re.DOTALL | re.MULTILINE)
    synonyms = dict_synonyms.get(word)
    synonyms_translate_html = None
    separate_synonyms = "-"*15
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
            
            html_stars = "".join([f"<span class='star-mini'></span>" for i in range(macmillan_stars)])
            translate_i = f"""<span class='synonym'>{word}</span><span class='ipa-margin'>{macmillan_ipa}</span>{html_stars} {translate_i}"""
            temp_translate = "".join([f"<div>{i}</div>" for i in translate_i.split("\n") if i])
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
            synonyms_translate_html = f"<div>{separate_synonyms}</div>".join(temp_list_html)        
        
    return synonyms_translate_html 

def get_word_building_linvinov(path_to_file):
    """
    Принимает на вход файл словобразование Литвинов, возвращает словарь слов и словарь групп
    """
    data_words = json.loads(get_data_file(path_to_file))
    data_groups = {}
    for word_i, val_i in data_words.items():
        group_i, translate_i = val_i.values()
        if not data_groups.get(group_i):
            data_groups[group_i] = []
        data_groups[group_i].append([word_i, translate_i])

    return data_words, data_groups

def get_synonyms_linvinov(path_to_file):
    """
    Принимает на вход файл синонимов Литвинов, возвращает словарь слов и словарь групп
    """
    data_words = json.loads(get_data_file(path_to_file))
    data_groups = {}
    for word_i, val_list_i in data_words.items():
        for val_i in val_list_i:
            translate_i, number_group_i, name_group_i, file_i = val_i
            if not data_groups.get(name_group_i):
                data_groups[name_group_i] = []
            data_groups[name_group_i].append([word_i, translate_i, number_group_i])

    return data_words, data_groups   

def get_html_for_synonyms_and_building(word, translate, add_html_code=""):
    """
    Возвращает верстку для синонимов и словообразования
    """
    macmillan_stars, macmillan_ipa = get_ipa_and_stars_macmillan(word)
    html_stars = "".join([f"<span class='star-mini'></span>" for i in range(macmillan_stars)])
    word_html = f"""<div onclick='myClick(this)'>
                        <span class="synonym">{word}</span>
                        <span class='ipa-margin'>{macmillan_ipa}</span>
                        {html_stars}
                        <span>{translate}</span>
                        
                        {add_html_code}
                    </div>"""
    return word_html                 

def get_synonyms_linvinov_html(word):
    """
    Возвращается все слова, входящие в одну группу с word
    """    
    info_word_list = word_synonyms_litvinov.get(word)
    synonyms_word = None
    temp = []
    if info_word_list: 
        for info_word_i in info_word_list:
            name_group = info_word_i[2]
            data_group_word = group_word_synonyms_litvinov.get(name_group)
            tmp_group = []
            for word_i, translate_i, number_group_i in data_group_word: 
                word_html = get_html_for_synonyms_and_building(word_i, translate_i)
                tmp_group.append(word_html)
            html_group = f"<div class='synonym'>{name_group}</div>" + "".join(tmp_group)
            temp.append(html_group)
        synonyms_word = "".join(temp)
    return synonyms_word    


def get_word_building_linvinov_html(word):
    """
    Возвращается все слова, входящие в одну группу с word
    """
    info_word = word_building_litvinov.get(word)
    building_word = None
    temp = []
    if info_word:
        data_group_word = group_word_building_litvinov.get(info_word["group"])
        for word_i, translate_i in data_group_word:
            word_html = get_html_for_synonyms_and_building(word_i, translate_i)                
            temp.append(word_html)                
        building_word = "".join(temp)    
    return building_word 

def get_ipa_and_stars_macmillan(word):
    """
    Возвращает число звезд и ipa
    """
    info_word = dict_macmillan.get(word)
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
        data_word = data_file.get(word)
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
                mnemo_html = "\n".join([f"<div>{i}</div>" for i in mnemo_list]) if mnemo_list else ""
                if word_i or mnemo_html:
                    html = f"<div>{translate}</div><div></div>{mnemo_html}"
                    html_trans_mnemo = html_temp.format(html=html) 

            info_word = get_html_for_synonyms_and_building(comment_i, "", html_trans_mnemo)

            comment_html.append(info_word)
        comment_html = "".join(comment_html)    
    return comment_html

def get_html_word(word, ipa, translate, mnemo_list, examples_list):
    synonyms = get_synonyms_html(word)
    synonyms_linvinov = get_synonyms_linvinov_html(word)
    word_building = get_word_building_linvinov_html(word)
    
    mnemo_html = "\n".join([f"<div>{i}</div>" for i in mnemo_list]) if mnemo_list else ""
    examples_html = "\n".join([f"<div>{i}</div>" for i in examples_list]) if examples_list else ""
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
    synonyms_litvinov_temp = synonyms_litvinov_temp.format(synonyms_linvinov=synonyms_linvinov) if synonyms_linvinov else ""   
    word_duilding_temp = word_duilding_temp.format(word_building=word_building) if word_building else ""
    examples_temp = examples_temp.format(examples=examples_html) if examples_html else ""
    stars_html = "".join([star_tmp for _ in range(macmillan_stars)])
    word_comment_temp = word_comment_temp.format(word_comment=word_comment_html) if word_comment_html else ""

    return base_html.format(word=word, 
                            ipa=ipa, 
                            stars=stars_html,
                            translate=translate, 
                            mnemo_temp=mnemo_temp, 
                            synonyms_temp=synonyms_temp, 
                            synonyms_litvinov_temp=synonyms_litvinov_temp,
                            word_duilding_temp=word_duilding_temp, 
                            word_comment_temp=word_comment_temp,
                            examples_temp=examples_temp)


def read_file(path_file):
    """
    Возврщает список слов для изучения
    """
    list_word = []
    for i in open(path_file, mode="r", encoding="utf-8"):
        list_word.append(i.split(";")[0].strip())
    return list_word

def generate_report_for_re(bot, template_word_i):
    
    def get_pattern(pattern):
        start_with = pattern.startswith("?")
        endswith = pattern.endswith("?")

        if start_with and endswith:
            pattern = rf".*?{pattern[1:-1]}.*"
            return pattern

        if pattern.startswith("?"):
            pattern = rf".*?{pattern[1:]}$"
        else:
            pattern = r"^" + pattern  
        
        if pattern.endswith("?"):
            pattern = pattern[0:-1] + r".*"
        return pattern    
    
    template_word_i = get_pattern(template_word_i)
        
    compl_pattern = re.compile(template_word_i, flags=re.DOTALL | re.MULTILINE)
    data_all_words = read_file(path_all_words)
    for word_i in data_all_words:
        search = compl_pattern.search(word_i)
        if search:
            data_word = parse_file(word_i)
            compression_data(name_base, data_word, table_name="words_of_template")

    send_report(bot, "words_of_template")
    send_report(bot, "words_of_template", "list")
    clear_table(name_base, "words_of_template")         


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
    

def generate_report_html(name_base, table_name):
    all_messages = []
    temp_html = get_data_file("test.html")

    for first_line, mnemo_srt, examples_str, error in fetchall(name_base, table_name):
        mnemo_list = mnemo_srt.split(separate) if mnemo_srt else []
        examples_list = examples_str.split(separate) if examples_str else []
        
        tmp_list = [i.strip() for i in first_line.split("|")]
        if len(tmp_list) == 3:
            word_i, transcription, translate = tmp_list
        else:
            raise Exception(f"В строке {first_line}\n должно быть два символа |")

        if not mnemo_list:
            mnemo_list = get_mnemo_list(word_i)    

        ipa=f"|{transcription}|"
        word_html = get_html_word(word_i, ipa, translate, mnemo_list, examples_list)

        all_messages.append(word_html)
    all_messages_text = "\n".join(all_messages)
    html_report = temp_html % (all_messages_text)
    html_report = html_report.encode("utf-8")

    return html_report

def get_list_words(name_base, table_name):
    """
    Возвращает список слов
    """
    list_words = []

    for first_line, mnemo_srt, examples_str, error in fetchall(name_base, table_name):
        tmp_list = [i.strip() for i in first_line.split("|")]
        word_i = "-"
        if len(tmp_list) == 3:
            word_i, transcription, translate = tmp_list
        list_words.append(word_i)
    return list_words    

def send_report(bot, table_name, type_report="html"):
    tmp_date = datetime.today().strftime(r"%d_%m_%Y")
    
    try:
        if type_report == "html":
            html_report = generate_report_html(name_base, table_name)
            with open(f"{path_to_save_reports}/report_{tmp_date}.html", mode="wb+") as f:
                f.write(html_report)
                for chat_id in config_bot.chat_id_list:
                    f.seek(0)
                    bot.send_document(chat_id, f) 
        elif type_report == "list":
            list_words = get_list_words(name_base, table_name)
            str_list_words = ', '.join([f'"{word_i}"' for word_i in list_words])
            text = f"[{str_list_words}]"
            send_message_from_bot(text)
        else:
            raise Exception("Передан неизвестный тип отчета")

    except Exception as e:
        print("Ошибка " + str(e))
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print("*** print_tb:")
        traceback.print_tb(exc_traceback) #, limit=1, file=sys.stdout

        with open(f"{path_to_save_reports}/report_error_{tmp_date}.txt", mode="wb+") as f:
            sep = "#" * 30
            data = ""
            for first_line, mnemo, _, err in fetchall(name_base, table_name):
                tmp_i = f"{first_line}\n\n{mnemo}\n{sep}\nError - {err}\n"
                data += tmp_i
            data_b = data.encode("utf-8")
            f.write(data_b)
            for chat_id in config_bot.chat_id_list:
                f.seek(0)
                bot.send_document(chat_id, f)     

def not_learn_word(word):
    with open(path_file_not_learn, encoding="utf-8", mode="a") as f:
        f.write(word + "\n")

def compression_data(name_base, data_word, table_name="words_of_day"):
    first_line, mnemo_list, examples_list, error = data_word
    temp = lambda l: separate.join(l)
    data_into = [(first_line, temp(mnemo_list), temp(examples_list), error)]
    into_table(name_base, data_into, table_name)


mnemo_garibjan = prepare_garibjan()
mnemo_galagoliya = prepare_galagoliya()

path_to_json_synonyms = os.path.join(path_synonyms_dir, "words.json")
dict_synonyms = json.loads(get_data_file(path_to_json_synonyms))

path_to_json_synonyms_litvinov = os.path.join(path_synonyms_dir, "litvinov_synonyms.json")
word_synonyms_litvinov, group_word_synonyms_litvinov = get_synonyms_linvinov(path_to_json_synonyms_litvinov)

path_to_litvinov_word_building = os.path.join(path_word_building_dir, "Литвинов.json") 
word_building_litvinov, group_word_building_litvinov = get_word_building_linvinov(path_to_litvinov_word_building)

dict_macmillan = json.loads(get_data_file("macmillan_ipa_stars.json"))  # содержит ipa и число звезд