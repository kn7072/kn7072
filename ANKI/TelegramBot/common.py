import config_bot
import requests
import os
import signal
from subprocess import Popen, PIPE
import re
import time
from config_bot import count_sound, path_dir_mp3, path_to_mplayer, time_sound_pause, path_dir, compl_mnemo, pattern_examples, schedule, path_anki
import pygame as pg
from datetime import datetime, timedelta
import datetime as dt


def send_message_from_bot(text):
    for chat_id in config_bot.chat_id_list:
        req_message = f"https://api.telegram.org/bot{config_bot.token}/sendMessage?chat_id={chat_id}&text={text}"
        #  print(req_message)
        res = requests.get(req_message)


def play_sound(word, volume=0.8):
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


def sound(word):
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
    path_file = os.path.join(path_dir, f"{word_i}.txt") 
    temp_list_msg = []
    try:
        with open(path_file, encoding="utf-8") as f:
            first_line = f.readline() 
            temp_list_msg.append(first_line)
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
            temp_list_msg.append(mnemo_text)    
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
                
            temp_list_msg.append(examples)        
    
    except Exception as e:
        print(e)
        temp_list_msg.append(str(e))

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
