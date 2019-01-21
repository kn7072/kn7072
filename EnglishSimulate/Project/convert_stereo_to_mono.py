# -*- coging: utf-8 -*-
import os
import subprocess

path_dir_stereo = r"longman_rus"
paht_dir_mono = r"longman_rus_mono"
paht_exp = r"EXPERIMEN"  # https://superuser.com/questions/314239/how-to-join-merge-many-mp3-files
path_clear_dir = "longman_rus_clear_meta"


def convert_stereo_mono(path_stereo, path_mono):
    commands = ["ffmpeg.exe", '-i', path_stereo, '-ac', '1', path_mono]
    process = subprocess.Popen(commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # print(" ".join(commands))
    process.wait(30)
    stdout, stderr = process.communicate()
    if not os.path.isfile(path_mono):
        print(path_mono)
    # if stdout:
    #     result = stdout.decode("cp1251").replace('\r', '').replace('\n', '')
    # else:
    #     raise Exception("При проверке подписи возникла ошибка\n%s" % stderr.decode("cp1251"))
    # return result

def create_meta_data():
    commands = ["ffmpeg.exe", '-i', path_stereo, '-ac', '1', path_mono]
    process = subprocess.Popen(commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # print(" ".join(commands))
    process.wait(30)
    stdout, stderr = process.communicate()
    if not os.path.isfile(path_mono):
        print(path_mono)
    pass

#bug_list = ["привет_rus.mp3", "между_тем_rus.mp3", "так_называемый_rus.mp3"]
for file_i in os.listdir(path_dir_stereo):  # os.listdir(path_dir_stereo)
    path_file_stereo = os.path.join(path_dir_stereo, file_i)
    path_file_mono = os.path.join(paht_dir_mono, file_i)
    convert_stereo_mono(path_file_stereo, path_file_mono)

print()
