# -*-coding:utf-8 -*-
import os
import re
import json

pattern = r"(?P<num>\d{1,3})\.(?P<rus>.+)"
temp_com = re.compile(pattern, re.S | re.M)

name_gerund_file = "gerund.json"
name_infinitive_file = "infinitive.json"
name_participle_file = "participle.json"

def get_data(path_file):
    temp_list_rus = []
    temp_list_eng = []

    with open(path_file, encoding="utf-8", mode="r") as f:
        data = json.loads(f.read())
        for i in data:
            rus_i, eng_i = i["rus"], i["eng"]
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

    return  temp_list_rus, temp_list_eng

def create_files(name, list_rus, list_eng):
    rus_name = "%s_RUS_PRINT.txt" % name
    eng_name = "%s_ENG_PRINT.txt" % name
    with open(rus_name, encoding="utf-8", mode="w") as f:
        f.write("\n".join(list_rus))

    with open(eng_name, encoding="utf-8", mode="w") as f:
        f.write("\n".join(list_eng))

temp_list_rus_g, temp_list_eng_g = get_data(name_gerund_file)
create_files("GERUND", temp_list_rus_g, temp_list_eng_g)


temp_list_rus_i, temp_list_eng_i = get_data(name_infinitive_file)
create_files("INFINITIVE", temp_list_rus_i, temp_list_eng_i)

temp_list_rus_p, temp_list_eng_p = get_data(name_participle_file)
create_files("PARTICIPLE", temp_list_rus_p, temp_list_eng_p)