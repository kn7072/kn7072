import config_bot
import requests
import os
import signal
from subprocess import Popen, PIPE
import re
import time
from config_bot import count_sound, path_dir_mp3, path_to_mplayer, time_sound_pause, path_dir, compl_mnemo, pattern_examples, schedule
import pygame as pg
from datetime import datetime


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


def parse_file(word_i, send_examples=False):
    path_file = os.path.join(path_dir, f"{word_i}.txt") 
    try:
        with open(path_file, encoding="utf-8") as f:
            first_line = f.readline() 
            send_message_from_bot(first_line)

            print(first_line) 
            next_data_file = f.read()

            search_mnemo = compl_mnemo.search(next_data_file)
            if search_mnemo:
                mnemo_text = search_mnemo.group("mnemo")
                print(mnemo_text)
                send_message_from_bot(mnemo_text)

                print("#" * 30)

            if send_examples:
                search_examples = re.findall(pattern_examples, next_data_file)
                if search_examples:
                    msg = "\n".join(search_examples)
                    send_message_from_bot(msg)
                else:
                    send_message_from_bot(next_data_file)    

            #print()    
    except Exception as e:
        print(e)

def next_play():
    """
    Определяем - нужно ли продолжать озвучивать слова в зависимости от расписания
    """
    current_datetime = datetime.today()    
    current_day = current_datetime.strftime('%A')  
    hour = current_datetime.hour
    minute = current_datetime.minute
    schedule_day = schedule[current_day]
    for schedule_i in schedule_day:
        start_hour, start_minute = [int(i) for i in schedule_i["start"].split(":")]
        stop_hour, stop_minute = [int(i) for i in schedule_i["stop"].split(":")]
        start_minute = start_minute if start_minute else 59
        stop_minute = stop_minute if stop_minute else 59
        
        if stop_hour < start_hour:
            msg = msg = f"Значение ключа start должно быть меньше значеня ключа stop\n Day {current_day}\n schedule:\n{schedule_i}"
            raise Exception(msg)
        else:
            if start_minute > stop_minute:
                msg = f"Значение ключа start должно быть меньше значеня ключа stop\n Day {current_day}\n schedule:\n{schedule_i}"
                raise Exception(msg)
        if hour >= start_hour and  hour <= stop_hour:
            
            if minute >= start_minute and  minute <= stop_minute:
                return True
    time.sleep(60)  # чтобы не вызывать слишком часто
    return False    

