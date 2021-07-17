import config_bot
import requests
import os
import signal
from subprocess import Popen, PIPE
import re
import time
from config_bot import count_sound, path_dir_mp3, path_to_mplayer, time_sound_pause, path_dir, compl_mnemo, pattern_examples, schedule, path_anki, path_file_not_learn, separate, name_base, path_synonyms_dir, path_word_building_dir, pattern_search_word_in_text
import pygame as pg
from datetime import datetime, timedelta
import datetime as dt
from db import into_table, fetchall
import json


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
    delimetr = "#"*30
    result = ""
    for i in mnemo_galagoliya:
        block_i = "\n".join(i)
        if word in block_i:
            list_temp.append(block_i)

    if list_temp:
        result = delimetr.join(list_temp)
    return result 

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
            translate_i = f"<span class='synonym'>{word}</span> {translate_i}"
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
        data_groups[group_i].append(f"{word_i} - {translate_i}")

    return data_words, data_groups

def get_word_building_linvinov_html(word):
    """
    Возвращается все слова, входящие в одну группу с word
    """
    info_word = word_building_litvinov.get(word)
    building_word = None
    if info_word:
        data_group_word = group_word_building_litvinov.get(info_word["group"])
        building_word = "".join([f"<div>{i}</div>" for i in data_group_word])
        
    return building_word 

def get_html_word(word, ipa, translate, mnemo_list, examples_list):
    synonyms = get_synonyms_html(word)
    word_building = get_word_building_linvinov_html(word)
    
    mnemo_html = "\n".join([f"<div>{i}</div>" for i in mnemo_list]) if mnemo_list else ""
    examples_html = "\n".join([f"<div>{i}</div>" for i in examples_list]) if examples_list else ""
    
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
                        {word_duilding_temp}
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

    mnemo_temp = mnemo_temp.format(mnemo=mnemo_html) if mnemo_html else "" 
    synonyms_temp = synonyms_temp.format(synonyms=synonyms) if synonyms else ""    
    word_duilding_temp = word_duilding_temp.format(word_building=word_building) if word_building else ""
    examples_temp = examples_temp.format(examples=examples_html) if examples_html else ""

    return base_html.format(word=word, 
                            ipa=ipa, 
                            translate=translate, 
                            mnemo_temp=mnemo_temp, 
                            synonyms_temp=synonyms_temp, 
                            word_duilding_temp=word_duilding_temp, 
                            examples_temp=examples_temp)


def send_report(bot):  # , message
    try:
        all_messages = []
        temp_html = get_data_file("test.html")
        tmp_date = datetime.today().strftime(r"%d_%m_%Y")
        
        for first_line, mnemo_srt, examples_str, error in fetchall(name_base):
            mnemo_list = mnemo_srt.split(separate) if mnemo_srt else []
            examples_list = examples_str.split(separate) if examples_str else []
            
            tmp_list = [i.strip() for i in first_line.split("|")]
            if len(tmp_list) == 3:
                word_i, transcription, translate = tmp_list
            else:
                raise Exception(f"В строке {first_line}\n должно быть два символа |")

            if not mnemo_list:
                garibjan = mnemo_garibjan.get(word_i, "")
                galagoliya = get_mnemo_galagoliya(word_i)
                mnemo = garibjan + "\n" + galagoliya
                mnemo_text = mnemo.replace("\xa0", "")
                mnemo_list = [i for i in mnemo_text.split("\n") if i]

            ipa=f"|{transcription}|"
            word_html = get_html_word(word_i, ipa, translate, mnemo_list, examples_list)

            all_messages.append(word_html)
        all_messages_text = "\n".join(all_messages)
        # html_report = temp_html.format(html_words=all_messages_text) 
        html_report = temp_html % (all_messages_text)
        html_report = html_report.encode("utf-8")
        with open(r"report_%s.html" % tmp_date, mode="wb+") as f:
            f.write(html_report)
            for chat_id in config_bot.chat_id_list:
                f.seek(0)
                bot.send_document(chat_id, f) 
    except Exception as e:
        print("Ошибка " + str(e))
        with open(r"report_error_%s.txt" % tmp_date, mode="wb+") as f:
            # data = "\n".join([" === ".join(i) for first_line, mnemo_list, _, _ in words_of_day])
            sep = "#" * 30
            data = ""
            for first_line, mnemo_list, _, err in fetchall(name_base):
                mnemo = "\n".join(mnemo_list)
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

def compression_data(name_base, data_word):
    first_line, mnemo_list, examples_list, error = data_word
    temp = lambda l: separate.join(l)
    data_into = [(first_line, temp(mnemo_list), temp(examples_list), error)]
    into_table(name_base, data_into)





mnemo_garibjan = prepare_garibjan()
mnemo_galagoliya = prepare_galagoliya()

path_to_json_synonyms = os.path.join(path_synonyms_dir, "words.json")
dict_synonyms = json.loads(get_data_file(path_to_json_synonyms))

path_to_litvinov_word_building = os.path.join(path_word_building_dir, "Литвинов.json") 
word_building_litvinov, group_word_building_litvinov = get_word_building_linvinov(path_to_litvinov_word_building)

