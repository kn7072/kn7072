#conding:utf-8
import os
import re

pattern = re.compile(r'^(?P<num>\d.?\.)', re.M|re.I)

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


def read_file_and_create_file():
    with open("temp_file.txt", encoding="utf-8") as f:
        data_file = f.readlines()
        first_line = data_file[0].replace("\n", "")
        file_name_to_save = first_line.replace(" ", "_") + ".txt"
        path_to_save = os.path.join("Литвинов", file_name_to_save)
        temp_data_to_save = data_file[1: ]
        count_str = len(temp_data_to_save)
        assert count_str % 2 == 0, "Число строк должно быть четным"
        middle_element = count_str // 2
        res = [(eng.replace("\n", ""), rus.replace("\n", "")) for eng, rus in zip(temp_data_to_save[: middle_element], temp_data_to_save[middle_element : ])]
        data_to_save_list = [f"{eng};{rus}" for eng, rus in res]
        data_to_save_text = "\n".join(data_to_save_list)

    with open(path_to_save, encoding="utf-8", mode="w") as f:
        f.write(data_to_save_text)    

    parse(res)

read_file_and_create_file()