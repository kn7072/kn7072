#coding:utf-8
import os
import re
import json

pattern = re.compile(r'(?P<num>\d.*?\.)', re.M|re.I)

list_dir_for_parse = ["./ЛитвиновСуществительное", "./ЛитвиновГлаголы",  "./ЛитвиновПрилагательные"]  # "./ЛитвиновГлаголы",  "./ЛитвиновПрилагательные"
litvinov_dict = {}

def create_file(name_file, data_file):
    with open(name_file, encoding="utf-8", mode="w") as f:
        for i in data_file:
            f.write(i)

def parse_json(path_to_json):
    with open(path_to_json, encoding="utf-8") as f:
        data_json = json.loads(f.read())
        for word_i, val_list_i in data_json.items():
            for val_i in val_list_i:
                val_i.append(path_to_json)
                if litvinov_dict.get(word_i):
                    litvinov_dict[word_i].append(val_i)
                    #print(word_i)
                else:
                    litvinov_dict[word_i] = []
                    litvinov_dict[word_i].append(val_i)
              

def parse_file_in_dir(path_to_dir):
    for name_file_i in os.listdir(path_to_dir):
        path_file_i = os.path.join(path_to_dir, name_file_i)
        name_file, ext = path_file_i.rsplit(".", 1)
        path_file_to_validate = name_file + ".txt"
        validate_file(path_file_to_validate)
        if ext == "json":
            continue
        parse_json(name_file + ".json")

def validate_file(path_to_file):
    for str_i in open(path_to_file, encoding="utf-8"):
        result = lambda str_i: pattern.search(str_i)
        res = result(str_i)
        if res:
            eng, rus = str_i.split(";")
            assert result(rus), f"{rus} должен содержать паттерт - {path_to_file}"
            assert result(eng), f"{eng} должен содержать паттерт - {path_to_file}"



for dir_i in list_dir_for_parse:
    res = parse_file_in_dir(dir_i)        

data_json = json.dumps(litvinov_dict, ensure_ascii=False, indent=4)
create_file("litvinov_synonyms.json", data_json)

for i in litvinov_dict["normal"]:
    print(i)    