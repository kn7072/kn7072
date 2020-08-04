# -*-coding:utf-8 -*-
import os
import re
import json

pattern = r"(?P<num>\d{1,3})\.(?P<rus>.+)"
temp_com = re.compile(pattern, re.S | re.M)

name_file = "exercise_answer.json"


def get_data(path_file):
    temp_list_rus = []
    temp_list_eng = []

    with open(path_file, encoding="utf-8", mode="r") as f:
        data = json.loads(f.read())
        for key_i, val_i in data.items():
            type_i, content_i = val_i["type"], val_i["content"]
            if type_i == "rus_eng":
                for i in content_i:
                    rus_i, eng_i = i[0], i[1]
                    findall_r = temp_com.findall(rus_i)
                    findall_e = temp_com.findall(eng_i)

                    if findall_r and len(findall_r[0]) == 2:
                        temp_list_rus.append(findall_r[0][1].strip())
                    else:
                        raise Exception

                    if findall_e and len(findall_e[0]) == 2:
                        temp_list_eng.append(findall_e[0][1].strip())
                    else:
                        raise Exception
            else:
                continue

    return  temp_list_rus, temp_list_eng

def create_files(name, list_rus, list_eng):
    rus_name = "%s_RUS_PRINT.txt" % name
    eng_name = "%s_ENG_PRINT.txt" % name
    with open(rus_name, encoding="utf-8", mode="w") as f:
        f.write("\n".join(list_rus))

    with open(eng_name, encoding="utf-8", mode="w") as f:
        f.write("\n".join(list_eng))

temp_list_rus_g, temp_list_eng_g = get_data(name_file)
create_files("EXERCISE", temp_list_rus_g, temp_list_eng_g)

