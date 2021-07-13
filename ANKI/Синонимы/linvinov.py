#conding:utf-8
import os
import re
import json

pattern = re.compile(r'^(?P<num>\d.?\.)', re.M|re.I)
name_temp_file = "temp_file.txt"
dir_name_for_save = "ЛитвиновСуществительное"

def parse(data_list):
    
    temp_dict = dict()
    number_group = None
    name_group = None

    def add_word(word, translate):
        if temp_dict.get(word):
            temp_dict[word].append([translate, number_group, name_group])
        else:
            temp_dict[word] = []
            temp_dict[word].append([translate, number_group, name_group])
    
    
    for eng, rus in data_list:
        result = pattern.search(eng)
        if result:
            number_group = result.group()
            name_group = rus.replace(number_group, "").strip()
            eng = eng.replace(number_group, "").strip()
            add_word(eng, name_group)
        else:
            add_word(eng, rus)
    return temp_dict


def read_file_and_create_file(strategy="default"):
    with open(name_temp_file, encoding="utf-8") as f:
        data_file = f.readlines()
        first_line = data_file[0].replace("\n", "")
        
        name_file = first_line.replace(" ", "_")
        file_name_to_save_txt = name_file + ".txt"
        path_to_save_txt = os.path.join(dir_name_for_save, file_name_to_save_txt)
        file_name_to_save_json = name_file + ".json"
        path_to_save_json = os.path.join(dir_name_for_save, file_name_to_save_json)
        
        temp_data_to_save = data_file[1: ]
        count_str = len(temp_data_to_save)
        assert count_str % 2 == 0, "Число строк должно быть четным"
        if strategy == "default":
            middle_element = count_str // 2
            res = [(eng.replace("\n", ""), rus.replace("\n", "")) for eng, rus in zip(temp_data_to_save[: middle_element], temp_data_to_save[middle_element : ])]
            data_to_save_list = [f"{eng};{rus}" for eng, rus in res]
        elif strategy == "rus_eng":
            res = [(eng.replace("\n", ""), rus.replace("\n", "")) for rus, eng  in zip(temp_data_to_save[0::2], temp_data_to_save[1::2])]
            data_to_save_list = [f"{eng};{rus}" for eng, rus in res]
            
        elif strategy == "eng_rus":
            res = [(eng.replace("\n", ""), rus.replace("\n", "")) for  eng, rus in zip(temp_data_to_save[0::2], temp_data_to_save[1::2])]
            data_to_save_list = [f"{eng};{rus}" for eng, rus in res]    
        
        data_to_save_text = "\n".join(data_to_save_list)

    with open(path_to_save_txt, encoding="utf-8", mode="w") as f:
        f.write(data_to_save_text) 

    with open(path_to_save_json, encoding="utf-8", mode="w") as f:
        dict_word = parse(res)
        f.write(json.dumps(dict_word, indent=4, ensure_ascii=False))       

    parse(res)

strategy = "default"
# strategy = "rus_eng"
#strategy = "eng_rus"
read_file_and_create_file(strategy=strategy)