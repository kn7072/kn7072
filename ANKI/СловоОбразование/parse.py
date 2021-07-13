#coding:utf-8
import os
import re
import json

name_file = "Литвинов.txt"
pattern = re.compile(r'^(?P<num>\d{1,4}.?\.)', re.M|re.I)

def parse_file(path_to_file):
    number_group = 0
    temp_dict = {}
    for str_i in open(path_to_file, encoding="utf-8"):
        result = pattern.search(str_i)
        if result:
            number_group = result.group()
            temp_str = str_i.replace(number_group, "").strip()
        else:
            temp_str = str_i.strip()
        try:
            eng, rus = temp_str.split("—")   
        except:
            print(temp_str) 
            raise  
        if "/" in eng:
            print(temp_str)  
            raise Exception(f"{temp_str}")  

        eng = eng.strip() 
        rus = rus.strip() 
        temp_dict[eng] = {}
        temp_dict[eng]["group"] = number_group
        temp_dict[eng]["translate"] = rus

    return temp_dict    

def create_file(path_file, data_file):
    with open(path_file, mode="w", encoding="utf-8") as f:
        f.write(data_file)

res = parse_file(name_file)
data_json = json.dumps(res, ensure_ascii=False, indent=4)
create_file("Литвинов.json", data_json)



