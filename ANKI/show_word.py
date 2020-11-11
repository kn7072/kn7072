# -*- coding: utf-8 -*-

import sys
from subprocess import Popen, PIPE
import os
import signal

path_dir = r"e:\kn7072_NEW\kn7072\ANKI\WORDS_NOTEPAD"
path_dir_mp3 = r"e:\kn7072_NEW\kn7072\EnglishSimulate\Project\sound_longman_mono"
path_to_mplayer = r"e:\ENG\mplayer\mplayer.exe"


def show_exercises(path_file_open):
    # "-qt 1111" -заполняет файл
    # , "-filePath D:\\kn7072\\ANKI\\FIRST.txt"
    # args = [r"C:\Program Files (x86)\Notepad++\notepad++.exe", "D:\\kn7072\\ANKI\\FIRST.txt","-multiInst", "-nosession",  "-qt 1111\n"]
    args = [r"C:\Program Files\Notepad++\notepad++.exe", path_file_open, "-multiInst", "-nosession"]
    # args = [r"nano", path_file_open]
    # args = [r"kate", path_file_open, "-n"]
    proc = Popen(args, stdout=PIPE, stderr=PIPE)
    return proc


def sound(word):
    # command = r"e:\ENG\mplayer\mplayer.exe  -delay -1 -loop 2  e:\kn7072_NEW\kn7072\EnglishSimulate\Project\sound_longman_mono\%s" % word
    # f = open("x", mode="w")
    # x = sys.stdout
    # sys.stdout = f
    try:
        path_sound_file = os.path.join(path_dir_mp3, f"{word}.mp3")
        # path_sound_file = "{ %s -loop 2}" % path_sound_file
        if not os.path.exists(path_sound_file):
            print(f"Не обнаружен файл {path_sound_file}")
        command_list = [path_to_mplayer, '-delay', '-2', '-loop', '2', path_sound_file]  #
        command_str = " ".join(command_list)
        print(command_str)
        # os.system(command_str)
        process = Popen(command_list)  #, stdout=subprocess.PIPE, stderr=subprocess.PIPE , shell=True, preexec_fn=os.setsid
        # process = subprocess.call(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(timeout=5)
        # print(stdout.decode())
        # exit_code = process.returncode
    except Exception as e:
        print(e)
        # process.kill()
        os.kill(process.pid, signal.SIGTERM)
        # os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    finally:
        # sys.stdout = x
        pass

# sound("yes")


while True:
    print("#" * 50)
    word = input("Введите слово:\n")
    print("#" * 50)
    if word == "q":
        sys.exit()
    else:
        file_path = os.path.join(path_dir, f"{word}.txt")
        try:
            # with open(file_path, mode="r", encoding="utf-8") as f:
            #     data_file = f.read()
            #     print(data_file)
            proc = show_exercises(file_path)
            sound(word)
            res = input()
            proc.kill()
        except:
            print(f"Не обранужено слово {file_path}")

