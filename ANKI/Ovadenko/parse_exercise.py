# coding=utf-8
import os
import re

number = "(?P<num>\d{1,2})\."
compl_number = re.compile(number)

path_to_file = "./Упражнения/6/2_eng"

def get_text_exercise(path_to_file: str) -> str: 
    all_text = ""
    for str_i in open(path_to_file, encoding="utf-8"):
        str_i = str_i.replace("\n", "")
        if str_i.endswith("-"):
            str_i = str_i[0: -1]
        else:
            str_i += " "
        all_text += str_i
    if not all_text:
        raise Exception(f"Пустой файл ${path_to_file}")
    return all_text

def get_list_sentance(text_exercise: str) -> list:
    res = compl_number.split(text_exercise)
    if not res[0]:
        res = res[1:]
    list_sentance = list(num + text for num, text in zip(res[0::2], res[1::2]))
    return list_sentance

def print_list_sentance(list_sentance):
    for i in list_sentance:
        print(i)

def get_files_of_dir(path_to_dir: str) -> list:
    temp_list = []
    for file_name in os.listdir(path_to_dir):
        if file_name.endswith("eng"):
            temp_list.append([file_name.replace("_eng", ""), file_name])
    return temp_list        

def create_file(path_to_file: str, data: str) -> None:
    with open(path_to_file, mode="w", encoding="utf-8") as f:
        f.write(data)

def read_file(path_to_file: str) -> str:
    with open(path_to_file, encoding="utf-8") as f:
        return f.read()        

# text_exerсise = get_text_exercise(path_to_file)
# print(text_exerсise)
# list_sentance = get_list_sentance(text_exerсise)
# print_list_sentance(list_sentance)